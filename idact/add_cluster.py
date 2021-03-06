# -*- coding: utf-8 -*-
"""Console script for idact-add-cluster.

How to run::

  python -m idact.add_cluster --help

.. click:: idact.add_cluster:main

"""

import sys
from idact.detail.add_cluster_app.main import main

if __name__ == "__main__":
    sys.exit(
        main())  # pragma: no cover, pylint: disable=no-value-for-parameter
