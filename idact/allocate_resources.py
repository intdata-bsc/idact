# -*- coding: utf-8 -*-
"""Console script for idact-allocate_resources.

How to run::

  python -m idact.allocate_resources --help

.. click:: idact.allocate_resources:main

"""

import sys
from idact.detail.allocate_resources_app.main import main

if __name__ == "__main__":
    sys.exit(
        main())  # pragma: no cover, pylint: disable=no-value-for-parameter
