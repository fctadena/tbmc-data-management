import json


def get_gid_from_json(file_path):
    # Open and read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Extract the value of gid
    gid = data['data'][0]['gid']
    return gid