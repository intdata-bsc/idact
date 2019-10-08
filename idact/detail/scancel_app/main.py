"""This module contains the :func:`main` canceling the slurm job, see :mod:`idact.scancel`.

 Note: The :func:`main` function uses :func:`click.command`, so it doesn't
 show up in API docs for this module. See help message in
 :mod:`idact.squeue`
 instead.

"""
import click

from idact import load_environment, show_cluster
from idact.detail.log.get_logger import get_logger
from idact.detail.slurm.run_scancel import run_scancel

@click.command()
@click.argument('cluster_name',
                type=str)
@click.argument('job_id',
                type=str)
def main(cluster_name: str,
         job_id: int) -> int:
    """A console script that cancels the slurm job.

        CLUSTER_NAME argument is the cluster name.
        It must already be present in the config file.

        JOB_ID argument is the id of the job to cancel
    """
    load_environment()
    log = get_logger(__name__)

    cluster = show_cluster(name=cluster_name)
    node = cluster.get_access_node()

    run_scancel(job_id, node)

    return 0
