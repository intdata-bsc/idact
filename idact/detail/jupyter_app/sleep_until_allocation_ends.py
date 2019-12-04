import os
from time import sleep

import click

from idact.core.nodes import Nodes

SLEEP_INTERVAL = 10


def sleep_until_allocation_ends(nodes: Nodes,
                                echo_messages: bool = True):
    """Sleeps until the allocation ends."""
    while nodes.running():
        if echo_messages:
            click.echo("Nodes are still running.")
        sleep(SLEEP_INTERVAL)

        if 'IDACT_TEST_NOTEBOOK_APP_TEST_RUN' in os.environ:
            if echo_messages:
                click.echo("This is a test run, cancelling the allocation.")
            nodes.cancel()

    if echo_messages:
        click.echo(click.style("Nodes are no longer running.", fg='red'))
