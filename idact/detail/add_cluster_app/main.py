"""This module contains the :func:`main` function for adding new cluster
 into local environment, see :mod:`idact.add_cluster`.

 Note: The :func:`main` function uses :func:`click.command`, so it doesn't
 show up in API docs for this module. See help message in
 :mod:`idact.add_cluster`
 instead.

"""
from typing import Optional
import click

from idact import AuthMethod, KeyType
from idact.core.add_cluster import add_cluster
from idact.core.environment import save_environment, load_environment
from idact.detail.log.get_logger import get_logger
from idact.detail.add_cluster_app import actions_parser as parser


@click.command()
@click.argument('cluster_name',
                type=str)
@click.argument('user',
                type=str)
@click.argument('host',
                type=str)
@click.option('--port', '-p',
              default=22,
              type=int,
              help="The ssh port. Default: 22")
@click.option('--auth',
              default=AuthMethod.PUBLIC_KEY,
              type=AuthMethod,
              help="Authentication method. Default: AuthMethod.PUBLIC_KEY")
@click.option('--key',
              default=KeyType.RSA,
              type=KeyType,
              help="Specified key type to be generated. "
                   "Default location: ~/.ssh")
@click.option('--install_key',
              default=True,
              is_flag=True,
              help="Flag for letting idact manage the key installation. "
                   "Default: True")
@click.option('--actions-file',
              default=None,
              type=str,
              help="In order for idact to find and execute the proper "
                   "binaries, they must be specified as a list of "
                   "Bash script lines.")
@click.option('--use-jupyter-lab',
              default=False,
              is_flag=True,
              help="Flag for using the jupyter lab instead of "
                   "jupyter notebook. "
                   "Default: False")
def main(cluster_name: str,
         user: Optional[str],
         host: Optional[str],
         port: Optional[int],
         auth: Optional[AuthMethod],
         key: Optional[KeyType],
         install_key: bool,
         actions_file: Optional[str],
         use_jupyter_lab: bool) -> int:
    """A console script that executes addition of cluster to environment.

        CLUSTER_NAME argument is the cluster name to be created.
        USER argument is the username for example 'plgtest'
        HOST argument is the host address for example 'pro.cyfronet.pl'

    """

    log = get_logger(__name__)

    log.info("Loading environment...")
    load_environment()

    log.info("Adding cluster...")
    cluster = add_cluster(name=cluster_name,
                          user=user,
                          host=host,
                          port=port,
                          auth=auth,
                          key=key,
                          install_key=install_key)

    node = cluster.get_access_node()
    node.connect()

    cluster.config.use_jupyter_lab = use_jupyter_lab

    if actions_file is not None:
        actions = parser.parse_actions(actions_file)
        cluster.config.setup_actions.jupyter = actions

    log.info("Saving environment...")
    save_environment()

    log.info("Cluster added.")
    return 0
