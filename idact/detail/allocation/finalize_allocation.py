import datetime
from typing import List

from idact.core.config import ClusterConfig
from idact.detail.allocation.allocation_parameters import AllocationParameters
from idact.detail.entry_point.fetch_port_info import fetch_port_info
from idact.detail.entry_point.remove_port_info import remove_port_info
from idact.detail.entry_point.sshd_port_info import SshdPortInfo
from idact.detail.helper.retry import retry
from idact.detail.nodes.node_impl import NodeImpl


def determine_ports_for_nodes(allocation_id: int,
                              hostnames: List[str],
                              config: ClusterConfig,
                              raise_on_missing: bool) -> List[int]:
    """Tries to determine sshd ports for each node.
        Removes the file if no exception was raised.

        :param allocation_id: Job id.

        :param hostnames: List of hostnames.

        :param config: Cluster config.

        :param raise_on_missing: Raise an exception if port could not
                                 be determined.

    """
    port_info_contents = fetch_port_info(allocation_id=allocation_id,
                                         config=config)
    port_info = SshdPortInfo(contents=port_info_contents)

    ports = [port_info.get_port(host=host,
                                raise_on_missing=raise_on_missing)
             for host in hostnames]
    remove_port_info(allocation_id, config=config)
    return ports


def finalize_allocation(allocation_id: int,
                        hostnames: List[str],
                        nodes: List[NodeImpl],
                        parameters: AllocationParameters,
                        allocated_until: datetime.datetime,
                        config: ClusterConfig):
    """Fetches node ports and makes them allocated.

        :param allocation_id: Allocation id, e.g. Slurm job id.

        :param hostnames: List of hostnames.

        :param nodes: Nodes to update with information.

        :param parameters: Allocation parameters.

        :param allocated_until: Timestamp for job termination.

        :param config: Cluster config.

    """

    def try_to_determine_ports():
        return determine_ports_for_nodes(allocation_id=allocation_id,
                                         hostnames=hostnames,
                                         config=config,
                                         raise_on_missing=True)

    try:
        ports = retry(try_to_determine_ports,
                      retries=config.port_info_retries,
                      seconds_between_retries=5)
    except RuntimeError:
        ports = determine_ports_for_nodes(allocation_id=allocation_id,
                                          hostnames=hostnames,
                                          config=config,
                                          raise_on_missing=False)

    for host, port, node in zip(hostnames, ports, nodes):
        node.make_allocated(
            host=host,
            port=port,
            cores=parameters.cores,
            memory=parameters.memory_per_node,
            allocated_until=allocated_until)
