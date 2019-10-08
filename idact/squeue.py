# -*- coding: utf-8 -*-
"""Console script for idact-squeue.

How to run::

  python -m idact.squeue --help

.. click:: idact.squeue:main

"""

import sys
from idact.detail.squeue_app.main import main

if __name__ == "__main__":
    sys.exit(
        main())  # pragma: no cover, pylint: disable=no-value-for-parameter
