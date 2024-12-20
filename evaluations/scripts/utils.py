import json
import pickle 

def read_json(path):
    """Function that reads JSON file"""

    with open(path, 'r') as file:
        data = json.load(file)

    return data

def load_pkl(filename):
    with open(filename, 'rb') as output:
        data = pickle.load(output)
    return data

def save_pkl(filename, data):
    with open(filename, 'wb') as output:
        pickle.dump(data, output)