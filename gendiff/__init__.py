import json


def generate_diff(path1, path2):
    data1 = json.load(open(path1))
    data2 = json.load(open(path2))
    data1_keys = set(data1.keys())
    data2_keys = set(data2.keys())
    all_keys = data1_keys.union(data2_keys)
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
    diff = "{{\n{}\n{}\n{}\n}}".format(
        "\n".join(additions), "\n".join(removals), "\n".join(changes)
    )
    return diff
