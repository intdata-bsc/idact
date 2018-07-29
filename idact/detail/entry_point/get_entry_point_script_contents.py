from idact.detail.auth.install_shared_home_key import SHARED_HOST_KEY_PATH
from idact.detail.config.client.client_cluster_config \
    import ClientClusterConfig
from idact.detail.entry_point.sshd_port_info import PORT_INFO_FILE_FORMAT, \
    PORT_INFO_LOCATION

COMPUTE_NODE_AUTHORIZED_KEYS = ".ssh/authorized_keys.idact"


def get_entry_point_script_contents(config: ClientClusterConfig) -> str:
    """Formats a full entry point command as the second tuple element.
       First tuple element is top-level environment set-up,
       i.e. to be executed before sbatch.
       Returned entry point will work correctly when enclosed in apostrophes.

       If the entry point deploys an sshd server, its port will be written
       to a file at PORT_INFO_LOCATION, named according to
       PORT_INFO_FILE_FORMAT.

        :param config: Cluster config.
    """

    if config.disable_sshd:
        entry_point = ("#!/usr/bin/env bash\n"
                       "trap : TERM INT; sleep infinity & wait")
    else:
        port_info_file = PORT_INFO_FILE_FORMAT.format(
            allocation_id="$IDACT_ALLOCATION_ID")
        entry_point = \
            ("#!/usr/bin/env bash\n"
             "SSHD_PORT=$(python -c 'import socket; s=socket.socket();"
             " s.bind((str(), 0)); print(s.getsockname()[1]);"
             " s.close()')\n"
             "mkdir -p {port_info_location}\n"
             "echo $(hostname):$SSHD_PORT"
             " >> {port_info_location}/{port_info_file}\n"
             " $(which sshd)"
             " -D "
             " -f /dev/null"
             " -oListenAddress=0.0.0.0"
             " -oPort=$SSHD_PORT"
             " -oHostKey={shared_host_key_path}"
             " -oPermitRootLogin=no"
             " -oStrictModes=yes"
             " -oPubkeyAuthentication=yes"
             " -oAuthorizedKeysFile={compute_node_authorized_keys}"
             " -oPasswordAuthentication=no"
             " -oChallengeResponseAuthentication=no"
             " -oKerberosAuthentication=no"
             " -oGSSAPIAuthentication=no"
             " -oUsePAM=no"
             " -oX11Forwarding=yes\n"
             "exit $?").format(shared_host_key_path=SHARED_HOST_KEY_PATH,
                               port_info_location=PORT_INFO_LOCATION,
                               port_info_file=port_info_file,
                               compute_node_authorized_keys=COMPUTE_NODE_AUTHORIZED_KEYS)  # noqa, pylint: disable=line-too-long

    return entry_point
