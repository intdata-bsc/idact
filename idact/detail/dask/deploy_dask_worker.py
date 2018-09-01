"""This module contains functionality for deploying a Dask worker."""

import re
from contextlib import ExitStack

import fabric.decorators

from idact.detail.dask.create_scratch_dir import create_scratch_subdir
from idact.detail.dask.dask_scheduler_deployment import DaskSchedulerDeployment
from idact.detail.dask.dask_worker_deployment import DaskWorkerDeployment
from idact.detail.dask.get_worker_deployment_script import \
    get_worker_deployment_script
from idact.detail.deployment.cancel_on_failure import cancel_on_failure
from idact.detail.deployment.create_deployment_dir import create_runtime_dir
from idact.detail.deployment.deploy_generic import deploy_generic
from idact.detail.helper.get_free_remote_port import get_free_remote_port
from idact.detail.helper.get_remote_file import get_remote_file
from idact.detail.helper.remove_runtime_dir \
    import remove_runtime_dir_on_failure
from idact.detail.helper.retry import retry
from idact.detail.log.get_logger import get_logger
from idact.detail.nodes.node_internal import NodeInternal
from idact.detail.tunnel.close_tunnel_on_failure import close_tunnel_on_failure

WORKER_VALIDATION_REGEX = r"Waiting to connect to:\s+?[^\s]+$"
__WORKER_VALIDATION_REGEX_COMPILED = re.compile(WORKER_VALIDATION_REGEX,
                                                re.MULTILINE)


def validate_worker_started(output: str):
    """Checks whether worker started correctly, according to the log.

        :param output: Dask worker output.

        :raises RuntimeError: When unable to validate.

    """

    match = __WORKER_VALIDATION_REGEX_COMPILED.search(output)
    if not match:
        raise RuntimeError("Unable to validate worker.")


def deploy_dask_worker(node: NodeInternal,
                       scheduler: DaskSchedulerDeployment) -> DaskWorkerDeployment:  # noqa, pylint: disable=line-too-long
    """Deploys a Dask worker on the node.

        :param node: Node to deploy on.

        :param scheduler: Already deployed scheduler.

    """
    log = get_logger(__name__)

    with ExitStack() as stack:
        runtime_dir = create_runtime_dir(node=node)
        stack.enter_context(
            remove_runtime_dir_on_failure(node=node,
                                          runtime_dir=runtime_dir))

        bokeh_port = get_free_remote_port(node=node)

        scratch_subdir = create_scratch_subdir(node=node)

        log_file = '{runtime_dir}/log'.format(runtime_dir=runtime_dir)

        script_contents = get_worker_deployment_script(
            scheduler_address=scheduler.address,
            bokeh_port=bokeh_port,
            scratch_subdir=scratch_subdir,
            cores=node.cores,
            memory_limit=node.memory,
            log_file=log_file,
            config=node.config)

        log.debug("Deployment script contents: %s", script_contents)
        deployment = deploy_generic(node=node,
                                    script_contents=script_contents,
                                    capture_output_seconds=5,
                                    runtime_dir=runtime_dir)
        stack.enter_context(cancel_on_failure(deployment))

        @fabric.decorators.task
        def validate_worker_started_from_log():
            """Checks that the worker has started correctly based on
                the log file."""
            output = get_remote_file(remote_path=log_file)
            log.debug("Log file: %s", output)
            validate_worker_started(output=output)

        retry(lambda: node.run_task(task=validate_worker_started_from_log),
              retries=5,
              seconds_between_retries=5)

        bokeh_tunnel = node.tunnel(there=bokeh_port)
        stack.enter_context(close_tunnel_on_failure(bokeh_tunnel))

        return DaskWorkerDeployment(deployment=deployment,
                                    bokeh_tunnel=bokeh_tunnel)