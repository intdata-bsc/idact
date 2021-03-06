import os
from contextlib import contextmanager
from logging import DEBUG

from idact import AuthMethod
from idact.core.retry import Retry
from idact.core.set_log_level import set_log_level
from idact.core.set_retry import set_retry
from idact.detail.config.client.client_cluster_config \
    import ClusterConfigImpl
from idact.detail.config.client.client_config import ClientConfig
from idact.detail.environment.environment_impl import EnvironmentImpl
from idact.detail.environment.environment_provider import EnvironmentProvider
from tests.helpers.clear_home import clear_home
from tests.helpers.get_default_retries_heavy_load import \
    get_default_retries_heavy_load
from tests.helpers.testing_environment import get_testing_host, \
    get_testing_port, TEST_CLUSTER, get_test_key_location, \
    get_test_environment_file


@contextmanager
def reset_environment(user: str, auth: AuthMethod = AuthMethod.ASK):
    """Clears the environment and adds the testing cluster.

        :param user: User to connect to the cluster as,
                     and whose home dir should be cleaned.

        :param auth: Authentication method to use.

    """
    # pylint: disable=protected-access
    saved_state = EnvironmentProvider._state
    EnvironmentProvider._state = None

    os.environ['IDACT_KEY_LOCATION'] = get_test_key_location(user=user)
    os.environ['IDACT_CONFIG_PATH'] = get_test_environment_file(user=user)

    cluster = ClusterConfigImpl(
        host=get_testing_host(),
        port=get_testing_port(),
        user=user,
        auth=auth,
        retries=get_default_retries_heavy_load())
    cluster.retries[Retry.PORT_INFO] = set_retry(count=0)

    EnvironmentProvider(
        initial_environment=EnvironmentImpl(
            config=ClientConfig(
                clusters={TEST_CLUSTER: cluster})))
    set_log_level(DEBUG)
    try:
        yield
    finally:
        EnvironmentProvider._state = saved_state
        clear_home(user=user)
