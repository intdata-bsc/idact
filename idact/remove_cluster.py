# -*- coding: utf-8 -*-
"""Console script for idact-remove-cluster.

How to run::

  python -m idact.remove_cluster --help

.. click:: idact.remove_cluster:main

"""

import sys
from idact.detail.remove_cluster_app.main import main

if __name__ == "__main__":
    sys.exit(
        main())  # pragma: no cover, pylint: disable=no-value-for-parameter
