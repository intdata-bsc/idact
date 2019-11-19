"""Contents of this module are intended to be imported into
   the top-level package.

   See :class:`.AuthMethod`, :class:`.KeyType`.
"""

from enum import Enum


class AuthMethod(Enum):
    """Cluster authentication methods.

        :attr:`.ASK`: Ask for password every time it's needed.

        :attr:`.GENERATE_KEY`: Generate a private and public key pair, and
                             install the public key.

        :attr:`.PRIVATE_KEY`: Authenticate with previously generated key

    """
    ASK = 0
    GENERATE_KEY = 1
    PRIVATE_KEY = 2


class KeyType(Enum):
    """Public key type."""
    RSA = 0
