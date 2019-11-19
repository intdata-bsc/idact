# -*- coding: utf-8 -*-
"""Console script for idact-deploy_notebook.

How to run::

  python -m idact.deploy_notebook --help

.. click:: idact.deploy_notebook:main

"""

import sys
from idact.detail.deploy_notebook_app.main import main

if __name__ == "__main__":
    sys.exit(
        main())  # pragma: no cover, pylint: disable=no-value-for-parameter
