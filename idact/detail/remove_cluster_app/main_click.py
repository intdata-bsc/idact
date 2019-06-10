"""This module contains the :func:`main` function for the quick Jupyter
 deployment app, see :mod:`idact.notebook`.

 Note: The :func:`main` function uses :func:`click.command`, so it doesn't
 show up in API docs for this module. See help message in :mod:`idact.notebook`
 instead.

"""

from idact import save_environment
from idact import remove_cluster
from idact.detail.remove_cluster_app import main as remove_cluster_app

import click

SNIPPET_SEPARATOR_LENGTH = 10


def main(cluster_name: str) -> int:
    """A console script that removes the cluster from the environment.

        CLUSTER_NAME argument is the cluster name.
        It must already be present in the config file.

    """
    remove_cluster_app.main(cluster_name=cluster_name)

    return 0
