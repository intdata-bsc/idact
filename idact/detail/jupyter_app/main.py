"""This module contains the :func:`main` function for the quick Jupyter
 deployment app, see :mod:`idact.notebook`.

 Note: The :func:`main` function uses :func:`click.command`, so it doesn't
 show up in API docs for this module. See help message in :mod:`idact.notebook`
 instead.

"""

from contextlib import ExitStack
from typing import Optional, List, Tuple

import click

from idact import load_environment, show_cluster, save_environment
from idact.detail.config.client.client_cluster_config import ClusterConfigImpl
from idact.detail.deployment.cancel_local_on_exit import cancel_local_on_exit
from idact.detail.deployment.cancel_on_exit import cancel_on_exit
from idact.detail.helper.ensure_stdin_has_fileno import \
    ensure_stdin_has_fileno
from idact.detail.jupyter_app.app_allocation_parameters import \
    AppAllocationParameters
from idact.detail.jupyter_app.format_allocation_parameters import \
    format_allocation_parameters
from idact.detail.jupyter_app.native_args_conversion import \
    convert_native_args_from_command_line_to_dict
from idact.detail.jupyter_app.override_parameters_if_possible import \
    override_parameters_if_possible
from idact.detail.jupyter_app.format_deployments_info import \
    format_deployments_info
from idact.detail.jupyter_app.sleep_until_allocation_ends import \
    sleep_until_allocation_ends
from idact.detail.log.get_logger import get_logger

SNIPPET_SEPARATOR_LENGTH = 10


def main(cluster_name: str,
         environment: Optional[str],
         save_defaults: bool,
         reset_defaults: bool,
         nodes: Optional[int],
         cores: Optional[int],
         memory_per_node: Optional[str],
         walltime: Optional[str],
         native_arg: List[Tuple[str, str]]) -> int:

    ensure_stdin_has_fileno()
    log = None
    try:
        with ExitStack() as stack:
            click.echo("Loading environment.")
            load_environment(path=environment)
            log = get_logger(__name__)

            cluster = show_cluster(name=cluster_name)
            config = cluster.config
            assert isinstance(config, ClusterConfigImpl)
            if reset_defaults:
                click.echo("Resetting allocation parameters to defaults.")
                config.notebook_defaults = {}
            parameters = AppAllocationParameters.deserialize(
                serialized=config.notebook_defaults)
            override_parameters_if_possible(parameters=parameters,
                                            nodes=nodes,
                                            cores=cores,
                                            memory_per_node=memory_per_node,
                                            walltime=walltime,
                                            native_args=native_arg)
            if save_defaults:
                click.echo("Saving defaults.")
                config.notebook_defaults = parameters.serialize()
                save_environment(path=environment)

            click.echo(format_allocation_parameters(parameters=parameters))

            click.echo("Allocating nodes.")
            nodes = cluster.allocate_nodes(
                nodes=parameters.nodes,
                cores=parameters.cores,
                memory_per_node=parameters.memory_per_node,
                walltime=parameters.walltime,
                native_args=convert_native_args_from_command_line_to_dict(
                    native_args=parameters.native_args))
            stack.enter_context(cancel_on_exit(nodes))
            nodes.wait()

            notebook = nodes[0].deploy_notebook()
            stack.enter_context(cancel_local_on_exit(notebook))

            click.echo("Pushing the allocation deployment.")
            cluster.push_deployment(nodes)

            click.echo("Pushing the notebook deployment.")
            cluster.push_deployment(notebook)

            click.echo(format_deployments_info(cluster_name=cluster_name))

            click.echo("Notebook address: ", nl=False)
            click.echo(click.style(notebook.address, fg='red'))
            notebook.open_in_browser()
            sleep_until_allocation_ends(nodes=nodes)
    except:  # noqa, pylint: disable=broad-except
        if log is not None:
            log.error("Exception raised.", exc_info=1)
            return 1
        raise
    return 0
