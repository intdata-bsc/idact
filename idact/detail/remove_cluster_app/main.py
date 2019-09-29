"""This module contains the :func:`main` function for the quick Jupyter
 deployment app, see :mod:`idact.notebook`.

 Note: The :func:`main` function uses :func:`click.command`, so it doesn't
 show up in API docs for this module. See help message in :mod:`idact.notebook`
 instead.

"""

from idact import save_environment
from idact import remove_cluster

import click

SNIPPET_SEPARATOR_LENGTH = 10


@click.command()
@click.argument('cluster_name',
                type=str)
def main(cluster_name: str) -> int:
    """A console script that removes the cluster from the environment.

        CLUSTER_NAME argument is the cluster name.
        It must already be present in the config file.

    """
    click.echo("Removing the cluster.")

    remove_cluster(cluster_name)

    save_environment()

    return 0
