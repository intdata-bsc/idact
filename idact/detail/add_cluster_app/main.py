"""This module contains the :func:`main` function for adding new cluster
 into local environment, see :mod:`idact.cluster`.

 Note: The :func:`main` function uses :func:`click.command`, so it doesn't
 show up in API docs for this module. See help message in :mod:`idact.cluster`
 instead.

"""
from typing import Optional
import click

from idact import AuthMethod, KeyType
from idact import add_cluster, save_environment, load_environment
from idact.detail.log.get_logger import get_logger


@click.command()
@click.argument('cluster_name',
                type=str)
@click.argument('user',
                type=str)
@click.argument('host',
                type=str)
# @click.option('--environment', '-e',
#               default=None,
#               type=str,
#               help="Environment path. Default: ~/.idact.conf"
#                    " or the value of IDACT_CONFIG_PATH.")
@click.option('--port', '-p',
              default=22,
              type=int,
              help="The ssh port. Default: 0")
@click.option('--auth',
              default=AuthMethod.PUBLIC_KEY,
              type=AuthMethod,
              help="Authentication method. Default: AuthMethod.PUBLIC_KEY")
@click.option('--key',
              default=KeyType.RSA,
              type=KeyType,
              help="Specified key type to be generated "
                   "(Default location: ~/.ssh)")
@click.option('--install_key',
              default=True,
              is_flag=True,
              help="Flag for letting idact manage the key installation.")
def main(cluster_name: str,
         user: Optional[str],
         host: Optional[str],
         port: Optional[int],
         auth: Optional[AuthMethod],
         key: Optional[KeyType],
         install_key: bool) -> int:
    """A console script that executes addition of cluster to environment.

        CLUSTER_NAME argument is the cluster name to be created.

    """

    log = get_logger(__name__)

    log.info("Loading environment...")
    load_environment()

    log.info("Adding cluster...")
    add_cluster(name=cluster_name,
                user=user,
                host=host,
                port=port,
                auth=auth,
                key=key,
                install_key=install_key)

    log.info("Saving environment...")
    save_environment()

    log.info("Cluster added.")
    return 0
