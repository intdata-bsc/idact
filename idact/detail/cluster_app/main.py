"""This module contains the :func:`main` function for adding new cluster
 into local environment, see :mod:`idact.cluster`.

 Note: The :func:`main` function uses :func:`click.command`, so it doesn't
 show up in API docs for this module. See help message in :mod:`idact.cluster`
 instead.

"""
from typing import Optional

import click

from idact import AuthMethod, KeyType

@click.command()
@click.argument('cluster_name',
                type=str)
@click.option('--user', '-u',
              default=None,
              type=str,
              help="The name of the user to log in as. Default: ''")
@click.option('--host',  '-h',
              default=None,
              type=str,
              help="The hostname of the login (head) node. Default: ''")
@click.option('--port',  '-p',
              default=None,
              type=int,
              help="The ssh port. Default: 0")
@click.option('--auth',
              default=None,
              type=AuthMethod,
              help="Authentication method. Default: AuthMethod.PUBLIC_KEY")
@click.option('--key',
              default=None,
              type=KeyType,
              help="Specified key type to be generated (Default location: ~/.ssh)")
@click.option('--install_key',
              is_flag=True,
              help="Flag for letting idact manage the key installation.")
def main(cluster_name: str,
         user: Optional[str],
         host: Optional[str],
         port: Optional[int],
         auth: Optional[AuthMethod],
         key: Optional[KeyType],
         install_key: bool,) -> int:
    """A console script that executes addition of cluster to environment.

        CLUSTER_NAME argument is the cluster name to be created.

    """

    return 0

