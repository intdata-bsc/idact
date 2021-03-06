"""Tests for core imports."""

from idact.core.set_log_level import set_log_level
from idact.core.node import Node
from idact.core.nodes import Nodes
from idact.core.auth import AuthMethod, KeyType
from idact.core.cluster import Cluster
from idact.core.add_cluster import add_cluster
from idact.core.show_clusters import show_cluster, show_clusters
from idact.core.walltime import Walltime
from idact.core.environment import load_environment, save_environment, \
    pull_environment, push_environment
from idact.core.tunnel import Tunnel
from idact.core.jupyter_deployment import JupyterDeployment
from idact.core.config import ClusterConfig, SetupActionsConfig, RetryConfig
from idact.core.dask_deployment import DaskDeployment, DaskDiagnostics
from idact.core.deploy_dask import deploy_dask
from idact.core.remove_cluster import remove_cluster
from idact.core.node_resource_status import NodeResourceStatus
from idact.core.synchronized_deployments import SynchronizedDeployments
from idact.core.get_default_retries import get_default_retries
from idact.core.retry import Retry
from idact.core.set_retry import set_retry

from idact import _IMPORTED
from idact import add_cluster as add_cluster2
from idact import show_cluster as show_cluster2
from idact import show_clusters as show_clusters2
from idact import load_environment as load_environment2
from idact import save_environment as save_environment2
from idact import AuthMethod as AuthMethod2
from idact import Cluster as Cluster2
from idact import Node as Node2
from idact import Nodes as Nodes2
from idact import Walltime as Walltime2
from idact import Tunnel as Tunnel2
from idact import JupyterDeployment as JupyterDeployment2
from idact import KeyType as KeyType2
from idact import set_log_level as set_log_level2
from idact import ClusterConfig as ClusterConfig2
from idact import SetupActionsConfig as SetupActionsConfig2
from idact import DaskDiagnostics as DaskDiagnostics2
from idact import DaskDeployment as DaskDeployment2
from idact import deploy_dask as deploy_dask2
from idact import remove_cluster as remove_cluster2
from idact import pull_environment as pull_environment2
from idact import push_environment as push_environment2
from idact import NodeResourceStatus as NodeResourceStatus2
from idact import SynchronizedDeployments as SynchronizedDeployments2
from idact import RetryConfig as RetryConfig2
from idact import get_default_retries as get_default_retries2
from idact import Retry as Retry2
from idact import set_retry as set_retry2

IMPORT_PAIRS_CORE_MAIN = [(add_cluster, add_cluster2),
                          (show_cluster, show_cluster2),
                          (show_clusters, show_clusters2),
                          (load_environment, load_environment2),
                          (save_environment, save_environment2),
                          (AuthMethod, AuthMethod2),
                          (Cluster, Cluster2),
                          (Node, Node2),
                          (Nodes, Nodes2),
                          (Walltime, Walltime2),
                          (Tunnel, Tunnel2),
                          (JupyterDeployment, JupyterDeployment2),
                          (KeyType, KeyType2),
                          (set_log_level, set_log_level2),
                          (ClusterConfig, ClusterConfig2),
                          (SetupActionsConfig, SetupActionsConfig2),
                          (DaskDiagnostics, DaskDiagnostics2),
                          (DaskDeployment, DaskDeployment2),
                          (deploy_dask, deploy_dask2),
                          (remove_cluster, remove_cluster2),
                          (pull_environment, pull_environment2),
                          (push_environment, push_environment2),
                          (NodeResourceStatus, NodeResourceStatus2),
                          (SynchronizedDeployments, SynchronizedDeployments2),
                          (RetryConfig, RetryConfig2),
                          (get_default_retries, get_default_retries2),
                          (Retry, Retry2),
                          (set_retry, set_retry2)]

CORE_IMPORTS = [add_cluster,
                load_environment,
                save_environment,
                show_cluster,
                show_clusters,
                AuthMethod,
                Cluster,
                Node,
                Nodes,
                Walltime,
                Tunnel,
                JupyterDeployment,
                KeyType,
                set_log_level,
                ClusterConfig,
                SetupActionsConfig,
                DaskDiagnostics,
                DaskDeployment,
                deploy_dask,
                remove_cluster,
                pull_environment,
                push_environment,
                NodeResourceStatus,
                SynchronizedDeployments,
                RetryConfig,
                get_default_retries,
                Retry,
                set_retry]


def test_aliases():
    """Tests classes and functions imported from the core package
       to the top level package.
    """
    assert len(_IMPORTED) == 28

    for core, main in IMPORT_PAIRS_CORE_MAIN:
        assert core is main

    main_module = 'idact'
    for core in CORE_IMPORTS:
        assert main_module == core.__module__
