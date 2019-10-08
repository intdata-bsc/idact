"""This module contains the :func:`main` function for removing the cluster
 from local environment, see :mod:`idact.remove_cluster`.

 Note: The :func:`main` function uses :func:`click.command`, so it doesn't
 show up in API docs for this module. See help message in
 :mod:`idact.remove_cluster`
 instead.

"""
import click

from idact import save_environment, load_environment
from idact.core.remove_cluster import remove_cluster
from idact.detail.log.get_logger import get_logger

SNIPPET_SEPARATOR_LENGTH = 10


@click.command()
@click.argument('cluster_name',
                type=str)
def main(cluster_name: str) -> int:
    """A console script that removes the cluster from the environment.

        CLUSTER_NAME argument is the cluster name.
        It must already be present in the config file.

    """
    log = get_logger(__name__)

    log.info("Loading environment...")
    load_environment()

    log.info("Removing cluster...")
    remove_cluster(cluster_name)

    log.info("Saving environment...")
    save_environment()

    log.info("Cluster removed.")
    return 0
