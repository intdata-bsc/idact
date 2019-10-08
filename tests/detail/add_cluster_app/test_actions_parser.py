"""Test for the parser of actions file."""
import os
from idact.detail.add_cluster_app import actions_parser as parser


def test_parse_bash_commands():
    # GIVEN
    with open("tmp-testfile", "w") as file:
        file.write("module load plgrid/tools/python-intel/3.6.2\n")
        file.write("module load plgrid/tools/python-intel/3.6.2")
        file.close()

    # WHEN
    list_of_actions = parser.parse_actions("tmp-testfile")

    # THEN
    assert list_of_actions == ["module load plgrid/tools/python-intel/3.6.2",
                               "module load plgrid/tools/python-intel/3.6.2"]

    os.remove("tmp-testfile")
