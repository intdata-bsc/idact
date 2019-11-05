"""This module contains the :func:`main` function for the quick Jupyter
 deployment app, see :mod:`idact.notebook`.

 Note: The :func:`main` function uses :func:`click.command`, so it doesn't
 show up in API docs for this module. See help message in :mod:`idact.notebook`
 instead.

"""

from contextlib import ExitStack

import click

from idact import load_environment, show_cluster
from idact.detail.allocation.allocation_parameters import AllocationParameters
from idact.detail.config.client.client_cluster_config import ClusterConfigImpl
from idact.detail.deployment.cancel_local_on_exit import cancel_local_on_exit
from idact.detail.helper.ensure_stdin_has_fileno import \
    ensure_stdin_has_fileno
from idact.detail.jupyter_app.format_deployments_info import \
    format_deployments_info
from idact.detail.jupyter_app.sleep_until_allocation_ends import \
    sleep_until_allocation_ends
from idact.detail.log.get_logger import get_logger
from idact.detail.nodes.get_access_node import get_access_node
from idact.detail.nodes.node_impl import NodeImpl
from idact.detail.nodes.nodes_impl import NodesImpl
from idact.detail.slurm.run_squeue import run_squeue
from idact.detail.slurm.slurm_allocation import SlurmAllocation
from idact.detail.slurm.squeue_result import SqueueResult

SNIPPET_SEPARATOR_LENGTH = 10


@click.command()
@click.argument('cluster_name',
                type=str)
@click.option('--job_id', '-e',
              default=None,
              type=int,
              help="ID of the job with allocated resources")
def main(cluster_name: str,
         job_id: int) -> int:
    """A console script that executes a Jupyter Notebook instance on
        an previously allocated resources

        CLUSTER_NAME argument is the cluster name to execute the notebook on.
        It must already be present in the config file.

        JOB_ID is the id of a job with previously allocated resources

    """
    ensure_stdin_has_fileno()
    log = None
    try:
        with ExitStack() as stack:
            click.echo("Loading environment.")
            load_environment()
            log = get_logger(__name__)

            cluster = show_cluster(name=cluster_name)
            config = cluster.config
            assert isinstance(config, ClusterConfigImpl)

            access_node = get_access_node(config=config)

            def run_squeue_task() -> SqueueResult:
                job_squeue = run_squeue(node=access_node)
                return job_squeue[job_id]

            job = run_squeue_task()

            node_count = job.node_count
            nodes_in_cluster = [NodeImpl(config=config) for _ in range(node_count)]

            entry_point_script_path = "~/.idact/entry_points"

            allocation = SlurmAllocation(
                job_id=job_id,
                access_node=access_node,
                nodes=nodes_in_cluster,
                entry_point_script_path=entry_point_script_path,
                parameters=AllocationParameters())

            nodes = NodesImpl(nodes=nodes_in_cluster,
                              allocation=allocation)

            notebook = nodes[0].deploy_notebook()
            stack.enter_context(cancel_local_on_exit(notebook))

            click.echo("Pushing the allocation deployment.")
            cluster.push_deployment(nodes)

            click.echo("Pushing the notebook deployment.")
            cluster.push_deployment(notebook)

            click.echo(format_deployments_info(cluster_name=cluster_name))

            click.echo("Notebook address: ", nl=False)
            click.echo(click.style(notebook.address, fg='red'))
            notebook.open_in_browser()
            sleep_until_allocation_ends(nodes=nodes)
    except:  # noqa, pylint: disable=broad-except
        if log is not None:
            log.error("Exception raised.", exc_info=1)
            return 1
        raise
    return 0
