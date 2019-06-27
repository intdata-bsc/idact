from click.testing import CliRunner
from idact.add_cluster import main as add_cluster_main
from idact.remove_cluster import main as remove_cluster_main
from tests.helpers.test_users import USER_64


def test_adding_and_removing_cluster():
    runner = CliRunner()
    user = USER_64

    result = runner.invoke(add_cluster_main, ['test-cluster ' + user + ' test-port'])
    assert 'Cluster added.' in result.output

    result = runner.invoke(remove_cluster_main, ['test-cluster'])
    assert 'Cluster removed.' in result.output

