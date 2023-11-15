import yaml

def read_config(config_file_path):
    with open(config_file_path, 'r') as file:
        return yaml.safe_load(file)

def write_config(config_file_path, config_data):
    with open(config_file_path, 'w') as file:
        yaml.dump(config_data, file, default_flow_style=False)

import os

def find_config_file():
    current_dir = os.getcwd()
    root_dir = os.path.abspath(os.sep)
    while current_dir != root_dir:
        config_file_path = os.path.join(current_dir, '.codereview', 'config.yaml')
        if os.path.isfile(config_file_path):
            return config_file_path
        current_dir = os.path.dirname(current_dir)
    raise FileNotFoundError("No '.codereview/config.yaml' found in any parent directories.")
