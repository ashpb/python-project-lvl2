import json
import yaml


def load_json(source):
    return json.load(source)


def load_yaml(source):
    return yaml.load(source, Loader=yaml.CLoader)


def determine_file_format(path):
    return path.split(sep=".")[-1].lower()


def load_file_contents(path):
    format = determine_file_format(path)
    with open(path, "r") as f:
        if format == "json":
            return load_json(f)
        elif format in ["yaml", "yml"]:
            return load_yaml(f)
        else:
            raise ValueError("Wrong file format")


def jsonify(value):
    """
    Converts value to JSON-compatible analog for output
    (i. e. True, False, None -> true, false, null)
    """
    return (
        json.JSONEncoder().encode(value) if type(value) is not str else value
    )
