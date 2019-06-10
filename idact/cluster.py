# -*- coding: utf-8 -*-
"""Console script for idact-cluster.

How to run::

  python -m idact.cluster --help

.. click:: idact.cluster:main

"""

import sys
from idact.detail.cluster_app.main_click import main

if __name__ == "__main__":
    sys.exit(
        main())  # pragma: no cover, pylint: disable=no-value-for-parameter
