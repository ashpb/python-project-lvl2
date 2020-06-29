from gendiff.io import load_file_contents, jsonify


def generate_diff_data(data1, data2):
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
    diff_data = dict()
    diff_data["additions"] = {key: data2.get(key) for key in added_keys}
    diff_data["removals"] = {key: data1.get(key) for key in removed_keys}
    diff_data["changes"] = {
        key: {"old": data1.get(key), "new": data2.get(key)}
        for key in changed_keys
    }
    diff_data["unchanged"] = {key: data1.get(key) for key in unchanged_keys}
    return diff_data


def output_diff(diff_data):
    additions = sorted(
        [
            "  + {key}: {value}".format(key=k, value=jsonify(v))
            for k, v in diff_data["additions"].items()
        ]
    )
    removals = sorted(
        [
            "  - {key}: {value}".format(key=k, value=jsonify(v))
            for k, v in diff_data["removals"].items()
        ]
    )
    changes = sorted(
        [
            "  - {key}: {old_value}\n  + {key}: {new_value}".format(
                key=k, old_value=jsonify(v["old"]), new_value=jsonify(v["new"])
            )
            for k, v in diff_data["changes"].items()
        ]
    )
    unchanged = sorted(
        [
            "    {key}: {value}".format(key=k, value=jsonify(v))
            for k, v in diff_data["unchanged"].items()
        ]
    )
    diff = "{{\n{}\n{}\n{}\n{}\n}}".format(
        "\n".join(unchanged),
        "\n".join(additions),
        "\n".join(removals),
        "\n".join(changes),
    )
    return diff


def generate_diff(file1, file2):
    return output_diff(
        generate_diff_data(
            load_file_contents(file1), load_file_contents(file2)
        )
    )
