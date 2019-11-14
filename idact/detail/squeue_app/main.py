"""This module contains the :func:`main` viewing information about jobs
located in the Slurm scheduling queue., see :mod:`idact.squeue`.

 Note: The :func:`main` function uses :func:`click.command`, so it doesn't
 show up in API docs for this module. See help message in
 :mod:`idact.squeue`
 instead.

"""
import click

from idact import load_environment, show_cluster
from idact.detail.log.get_logger import get_logger
from idact.detail.slurm.run_squeue import run_squeue


@click.command()
@click.argument('cluster_name',
                type=str)
def main(cluster_name: str) -> int:
    """A console script that shows information about jobs located in the Slurm
       scheduling queue.

        CLUSTER_NAME argument is the cluster name.
        It must already be present in the config file.
    """
    load_environment()
    log = get_logger(__name__)

    cluster = show_cluster(name=cluster_name)
    node = cluster.get_access_node()
    jobs = run_squeue(node)

    for job_id in jobs.keys():
        log.info(jobs[job_id])

    return 0
