# -*- coding: utf-8 -*-
"""Console script for idact-scancel.

How to run::

  python -m idact.scancel --help

.. click:: idact.scancel:main

"""

import sys
from idact.detail.scancel_app.main import main

if __name__ == "__main__":
    sys.exit(
        main())  # pragma: no cover, pylint: disable=no-value-for-parameter
