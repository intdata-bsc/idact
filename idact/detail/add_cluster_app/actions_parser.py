def parse_actions(file_name: str):
    """ Parser for the actions file.
    The file should contain bash commands
    line after line.
    """
    with open(file_name) as file:
        list_of_actions = file.read().split('\n')
    return list_of_actions
