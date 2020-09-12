from gendiff.io import load_file_contents, jsonify
from collections import namedtuple


def generate_diff_data(data1, data2):
    """
    Generates internal representation of difference
    between two data structures
    """
    DiffKey = namedtuple("DiffKey", ["status", "name"])
    common_keys = data1.keys() & data2.keys()
    added_keys = data2.keys() - data1.keys()
    removed_keys = data1.keys() - data2.keys()
    diff_data = dict()
    for k in common_keys:
        if data1[k] == data2[k]:
            diff_data[DiffKey(status="unchanged", name=k)] = data1[k]
        elif data1[k] != data2[k]:
            if isinstance(data1[k], dict) and isinstance(data2[k], dict):
                diff_data[
                    DiffKey(status="unchanged", name=k)
                ] = generate_diff_data(data1[k], data2[k])
            else:
                diff_data[DiffKey(status="changed", name=k)] = {
                    "old": data1[k],
                    "new": data2[k],
                }
    for k in removed_keys:
        diff_data[DiffKey(status="removed", name=k)] = data1[k]
    for k in added_keys:
        diff_data[DiffKey(status="added", name=k)] = data2[k]
    return diff_data


def _render_value(value, indent_level=0):
    """
    Recursively renders string representation of a dict value
    (the value might itself be a dict). This is a helper function
    used by 'render_diff' function.
    """
    padding = "    " * indent_level
    if isinstance(value, dict):
        items = sorted(
            [
                "{0}        {1}: {2}".format(
                    padding, k, _render_value(v, indent_level=indent_level + 1)
                )
                for k, v in value.items()
            ]
        )
        return "{{\n{0}\n{1}    }}".format("\n".join(items), padding)
    else:
        return jsonify(value)


def render_diff(diff_data, indent_level=0):
    """
    Recursively renders string representation of difference
    between two data structures. The diffenence data is expected to be
    in the format provided by 'generate_diff_data' function.
    """
    padding = "    " * indent_level
    readable_diff = "{\n"
    for k in sorted(diff_data.keys(), key=lambda k: k.name):
        if isinstance(diff_data[k], dict) and k.status == "unchanged":
            readable_diff += "{0}    {1}: {2}\n".format(
                padding,
                k.name,
                render_diff(diff_data[k], indent_level=indent_level + 1),
            )
        elif k.status == "changed":
            readable_diff += "{0}  - {1}: {2}\n".format(
                padding,
                k.name,
                _render_value(diff_data[k]["old"], indent_level=indent_level),
            )
            readable_diff += "{0}  + {1}: {2}\n".format(
                padding,
                k.name,
                _render_value(diff_data[k]["new"], indent_level=indent_level),
            )
        elif k.status == "added":
            readable_diff += "{0}  + {1}: {2}\n".format(
                padding,
                k.name,
                _render_value(diff_data[k], indent_level=indent_level),
            )
        elif k.status == "removed":
            readable_diff += "{0}  - {1}: {2}\n".format(
                padding,
                k.name,
                _render_value(diff_data[k], indent_level=indent_level),
            )
        else:
            readable_diff += "{0}    {1}: {2}\n".format(
                padding,
                k.name,
                _render_value(diff_data[k], indent_level=indent_level),
            )
    readable_diff += "{0}}}".format(padding)
    return readable_diff


def generate_diff(file1_path, file2_path):
    """
    Generates human-readable diff between two files.
    JSON and YAML files are supported at the moment.
    """
    return render_diff(
        generate_diff_data(
            load_file_contents(file1_path), load_file_contents(file2_path)
        )
    )
