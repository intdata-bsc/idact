def parse_actions(file_name: str):
    """

    """
    with open(file_name) as f:
        list_of_actions = f.readlines()
    return list_of_actions

