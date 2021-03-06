from contextlib import contextmanager

from typing import Any


@contextmanager
def cancel_local_on_exit(obj: Any):
    """A context manager that calls cancel_local on the object on context exit.

        :param obj: Object to execute cancel_local on.
    """
    try:
        yield
    finally:
        obj.cancel_local()
