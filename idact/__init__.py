# -*- coding: utf-8 -*-

"""
idact package
=============

Top-level package for Interactive Data Analysis Convenience Tools.
"""
from idact.core.auth import AuthMethod, KeyType
from idact.core.environment import load_environment, save_environment
from idact.core.jupyter_deployment import JupyterDeployment
from idact.core.nodes import Nodes, Node
from idact.core.set_log_level import set_log_level
from idact.core.show_clusters import show_cluster, show_clusters
from idact.core.tunnel import Tunnel
from idact.core.walltime import Walltime
from idact.core.add_cluster import add_cluster
from idact.core.cluster import Cluster

__author__ = """Matt Garstka"""
__email__ = 'matt.garstka@gmail.com'
__version__ = '0.1.0'

_IMPORTED = {add_cluster,
             load_environment,
             save_environment,
             show_cluster,
             show_clusters,
             AuthMethod,
             Cluster,
             Walltime,
             Node,
             Nodes,
             Tunnel,
             JupyterDeployment,
             KeyType,
             set_log_level}
"""List of the public API members imported into the top level package
   for convenience."""


def _patch_modules_for_sphinx():
    """Sphinx looks at the __module__ attribute to determine the module
       of a class, function, etc. while generating documentation.

       This value does not change after importing the object into the top
       level package, even if this effectively makes the object its member.

       In order for Sphinx to show the imported objects as members
       of the top level package, the __module__ attribute is changed manually
       for all imported objects.
    """
    for imported in _IMPORTED:
        imported.__module__ = 'idact'


_patch_modules_for_sphinx()
