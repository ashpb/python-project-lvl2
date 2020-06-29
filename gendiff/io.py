import json
import yaml


# def custom_json_decoder(obj):
#     """
#     Prevents conversion of 'true', 'false', 'null' and other non-string
#     values to their Python equivalents.
#     """
#     return {
#         k: json.JSONEncoder().encode(v) if type(v) is not str else v
#         for k, v in obj.items()
#     }


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
