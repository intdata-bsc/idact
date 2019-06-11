"""This module contains the :func:`main` function for adding new cluster
 into local environment, see :mod:`idact.cluster`.

 Note: The :func:`main` function uses :func:`click.command`, so it doesn't
 show up in API docs for this module. See help message in :mod:`idact.cluster`
 instead.

"""
from typing import Optional

from idact import AuthMethod, KeyType
from idact import add_cluster
from idact import save_environment, load_environment


def main(cluster_name: str,
         user: Optional[str],
         host: Optional[str],
         port: Optional[int],
         auth: Optional[AuthMethod],
         key: Optional[KeyType],
         install_key: bool) -> int:

    load_environment()

    add_cluster(name=cluster_name,
                user=user,
                host=host,
                port=port,
                auth=auth,
                key=key,
                install_key=install_key)

    save_environment()

    return 0

