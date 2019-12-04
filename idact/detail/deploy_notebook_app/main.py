"""This module contains the :func:`main` function for the quick Jupyter
 deployment app on previously allocated resources,
  see :mod:`idact.deploy_notebook`.

 Note: The :func:`main` function uses :func:`click.command`, so it doesn't
 show up in API docs for this module.
 See help message in :mod:`idact.deploy_notebook`
 instead.

"""

from contextlib import ExitStack

import click

from idact import load_environment, show_cluster
from idact.detail.allocation.finalize_allocation import finalize_allocation
from idact.detail.config.client.client_cluster_config import ClusterConfigImpl
from idact.detail.deployment.cancel_local_on_exit import cancel_local_on_exit
from idact.detail.helper.ensure_stdin_has_fileno import \
    ensure_stdin_has_fileno
from idact.detail.jupyter_app.format_deployments_info import \
    format_deployments_info
from idact.detail.jupyter_app.sleep_until_allocation_ends import \
    sleep_until_allocation_ends
from idact.detail.log.get_logger import get_logger
from idact.detail.slurm.run_squeue import run_squeue

SNIPPET_SEPARATOR_LENGTH = 10


@click.command()
@click.argument('cluster_name',
                type=str)
@click.argument('job_id',
                type=int)
def main(cluster_name: str,
         job_id: int) -> int:
    """A console script that executes a Jupyter Notebook instance on
        previously allocated resources

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

            squeue = run_squeue(cluster.get_access_node())
            deployments = cluster.pull_deployments()
            target_nodes = None

            for nodes_collection in deployments.nodes:
                if nodes_collection.allocation.job_id == job_id:
                    if job_id not in squeue:
                        click.echo('Cannot deploy notebook. Job is not in the queue.')
                        return 0
                    elif nodes_collection.nodes[0].host is None \
                            and squeue[job_id].node_list is not None \
                            and squeue[job_id].state == 'RUNNING':
                        finalize_allocation(allocation_id=job_id,
                                            hostnames=squeue[job_id].node_list,
                                            nodes=nodes_collection.nodes,
                                            parameters=nodes_collection.allocation.parameters,
                                            allocated_until=squeue[job_id].end_time,
                                            config=cluster.config)
                        nodes_collection.allocation.waited = True
                        cluster.push_deployment(nodes_collection)

                    target_nodes = nodes_collection

            if target_nodes is None:
                click.echo('Cannot deploy notebook. Nodes not found in deployments.')
                return 0

            for node in target_nodes:
                for jupyter_deployment in deployments.jupyter_deployments:
                    if node == jupyter_deployment.deployment.node:
                        click.echo('Jupyter Notebook is already started. It will be opened in the browser.')
                        jupyter_deployment.open_in_browser()
                        return 0

            notebook = target_nodes[0].deploy_notebook()
            stack.enter_context(cancel_local_on_exit(notebook))
            click.echo("Pushing the notebook deployment.")
            cluster.push_deployment(notebook)
            click.echo(format_deployments_info(cluster_name=cluster_name))
            click.echo("Notebook address: ", nl=False)
            click.echo(click.style(notebook.address, fg='red'))
            notebook.open_in_browser()
            sleep_until_allocation_ends(nodes=target_nodes)

    except:  # noqa, pylint: disable=broad-except
        if log is not None:
            log.error("Exception raised.", exc_info=1)
            return 1
        raise
    return 0
