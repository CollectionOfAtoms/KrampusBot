import yaml

def load_yaml(filename):
    """
    Load YAML data from a file.

    :param filename: The path to the YAML file.
    :return: The data loaded from the YAML file.
    """
    try:
        with open(filename, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Error loading YAML file: {e}")
        return None