"""Sample CLI test."""

from click.testing import CliRunner

from idact.cluster import main


def test_no_cluster_name():
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 2
    print(result.output)
    assert 'Usage: cluster.py [OPTIONS] CLUSTER_NAME USER HOST\n' in result.output
    assert 'Error: Missing argument' in result.output


def test_help():
    runner = CliRunner()
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    print(result.output)
    assert 'A console script that executes addition of cluster to environment.' \
           in result.output
    assert 'Show this message and exit.' in result.output
