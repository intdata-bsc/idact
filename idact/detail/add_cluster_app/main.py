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
              default='PUBLIC_KEY',
              type=str,
              help="Authentication method. Avilable values: PUBLIC_KEY, ASK_EVERYIME. "
              "Default: PUBLIC_KEY")
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
                   "Bash script lines. "
                   "NOTE: RuntimeError: Retried and failed: config.retries[Retry.JUPYTER_JSON]."
                   "{count=15, seconds_between=1} could be caused by not specifying this file.")
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

    if auth == 'PUBLIC_KEY':
        auth_method = AuthMethod.PUBLIC_KEY
        key_type = KeyType.RSA
        cluster = add_cluster(name=cluster_name,
                              user=user,
                              host=host,
                              port=port,
                              auth=auth_method,
                              key=key_type,
                              install_key=install_key)
    elif auth == 'ASK_EVERYIME':
        auth_method = AuthMethod.ASK
        cluster = add_cluster(name=cluster_name,
                              user=user,
                              host=host,
                              port=port,
                              auth=auth_method,
                              install_key=install_key)
    else:
        raise ValueError("Auth must be one of: PUBLIC_KEY, ASK_EVERYIME")

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
