def parse_actions(file_name: str):
    """ Parser for the actions file.
    The file should contain bash commands
    line after line.
    """
    with open(file_name, 'r') as actions_file:
        list_of_actions = actions_file.read().split('\n')
    return list_of_actions
