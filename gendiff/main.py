import json


def custom_json_decoder(obj):
    """
    Prevents conversion of 'true', 'false', 'null' and other non-string
    values to their Python equivalents.
    """
    return {
        k: json.JSONEncoder().encode(v) if type(v) is not str else v
        for k, v in obj.items()
    }


def generate_diff(path1, path2):
    data1 = json.load(open(path1), object_hook=custom_json_decoder)
    data2 = json.load(open(path2), object_hook=custom_json_decoder)
    data1_keys = set(data1.keys())
    data2_keys = set(data2.keys())
    all_keys = data1_keys.union(data2_keys)
    unchanged_keys = set()
    added_keys = set()
    removed_keys = set()
    changed_keys = set()
    for k in all_keys:
        if (k not in data1_keys) and (k in data2_keys):
            added_keys.add(k)
        elif (k in data1_keys) and (k not in data2_keys):
            removed_keys.add(k)
        elif (
            (k in data1_keys)
            and (k in data2_keys)
            and (data1.get(k) != data2.get(k))
        ):
            changed_keys.add(k)
        else:
            unchanged_keys.add(k)
    additions = [
        "  + {key}: {value}".format(key=k, value=data2.get(k))
        for k in added_keys
    ]
    removals = [
        "  - {key}: {value}".format(key=k, value=data1.get(k))
        for k in removed_keys
    ]
    changes = [
        "  - {key}: {old_value}\n  + {key}: {new_value}".format(
            key=k, old_value=data1.get(k), new_value=data2.get(k)
        )
        for k in changed_keys
    ]
    unchanged = [
        "    {key}: {value}".format(key=k, value=data1.get(k))
        for k in unchanged_keys
    ]
    diff = "{{\n{}\n{}\n{}\n{}\n}}".format(
        "\n".join(unchanged),
        "\n".join(additions),
        "\n".join(removals),
        "\n".join(changes),
    )
    return diff
