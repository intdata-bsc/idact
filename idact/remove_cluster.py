# -*- coding: utf-8 -*-
"""Console script for idact-remove_cluster.

How to run::

  python -m idact.remove_cluster --help

Or::

  idact-notebook --help

.. click:: idact.notebook:main
   :prog: idact-notebook
   :show-nested:

"""

import sys
from idact.detail.remove_cluster_app.main import main

if __name__ == "__main__":
    sys.exit(
        main())  # pragma: no cover, pylint: disable=no-value-for-parameter
