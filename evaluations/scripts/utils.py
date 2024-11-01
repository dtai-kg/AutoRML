import json

def read_json(path):
    """Function that reads JSON file"""

    with open(path, 'r') as file:
        data = json.load(file)

    return data