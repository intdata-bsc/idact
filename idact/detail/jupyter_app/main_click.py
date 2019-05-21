"""This module contains the :func:`main` function for the quick Jupyter
 deployment app, see :mod:`idact.notebook`.

 Note: The :func:`main` function uses :func:`click.command`, so it doesn't
 show up in API docs for this module. See help message in :mod:`idact.notebook`
 instead.

"""

from typing import Optional, List, Tuple
import click
from idact.detail.jupyter_app import main as deploy_notebook

SNIPPET_SEPARATOR_LENGTH = 10


@click.command()
@click.argument('cluster_name',
                type=str)
@click.option('--environment', '-e',
              default=None,
              type=str,
              help="Environment path. Default: ~/.idact.conf"
                   " or the value of IDACT_CONFIG_PATH.")
@click.option('--save-defaults',
              is_flag=True,
              help="Save allocation parameters as defaults for next time.")
@click.option('--reset-defaults',
              is_flag=True,
              help="Reset unspecified allocation parameters to defaults.")
@click.option('--nodes',
              default=None,
              type=int,
              help="Cluster node count. [Allocation parameter]."
                   " Jupyter notebook will be deployed on the first node."
                   " Default: 1.")
@click.option('--cores',
              default=None,
              type=int,
              help="CPU core count per node. [Allocation parameter]."
                   " Default: 1")
@click.option('--memory-per-node',
              default=None,
              type=str,
              help="Memory per node. [Allocation parameter]."
                   " Default: 1GiB")
@click.option('--walltime',
              default=None,
              type=str,
              help="Maximum time to allocate"
                   " the resources for. Format: [days-]hours:minutes:seconds."
                   " [Allocation parameter]."
                   " Default: 0:10:00")
@click.option('--native-arg',
              nargs=2,
              multiple=True,
              type=str,
              metavar='ARG VALUE',
              default=[],
              help="Native arguments for the workload manager."
                   " Flags have value=None, e.g. --native-arg --flag None."
                   " Can be repeated for multiple native args:"
                   " --native-arg -arg1 v1 --native-arg -arg2 v2 (...)."
                   " Values are not validated."
                   " Supported arguments take precedence over native"
                   " arguments."
                   " Arguments specified later override earlier arguments."
                   " [Allocation parameter]."
                   " Default: No native arguments.")
def main(cluster_name: str,
         environment: Optional[str],
         save_defaults: bool,
         reset_defaults: bool,
         nodes: Optional[int],
         cores: Optional[int],
         memory_per_node: Optional[str],
         walltime: Optional[str],
         native_arg: List[Tuple[str, str]]) -> int:
    """A console script that executes a Jupyter Notebook instance on
        an allocated cluster node, and makes it accessible
        in the local browser.

        CLUSTER_NAME argument is the cluster name to execute the notebook on.
        It must already be present in the config file.

    """
    deploy_notebook.main(cluster_name=cluster_name,
                         environment=environment,
                         save_defaults=save_defaults,
                         reset_defaults=reset_defaults,
                         nodes=nodes,
                         cores=cores,
                         memory_per_node=memory_per_node,
                         walltime=walltime,
                         native_arg=native_arg)
