"""This module contains the implementation of a multi hop SSH tunnel."""
from contextlib import ExitStack
from typing import List

from idact.core.tunnel import Tunnel
from idact.detail.tunnel.close_tunnel_on_exit import close_tunnel_on_exit


class MultiHopTunnel(Tunnel):
    """Tunnel consisting of one or multiple segments.

        :param tunnels: Tunnel segments.

    """

    def __init__(self, tunnels: List[Tunnel]):
        if not tunnels:
            raise ValueError(
                "Multi-hop tunnel requires at least one tunnel segment.")
        self._tunnels = tunnels
        self._here = tunnels[-1].here
        self._there = tunnels[-1].there

    @property
    def there(self) -> int:
        return self._there

    @property
    def here(self) -> int:
        return self._here

    def close(self):
        with ExitStack() as stack:
            for i in self._tunnels:
                stack.enter_context(close_tunnel_on_exit(i))

    def __str__(self):
        return "{class_name}({here}:{there})".format(
            class_name=self.__class__.__name__,
            here=self.here,
            there=self.there)

    def __repr__(self):
        return str(self)
