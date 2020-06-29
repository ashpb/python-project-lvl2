from gendiff.main import generate_diff


def test_flat_json_diff():
    with open("tests/fixtures/flat_diff.txt") as f:
        diff = f.read()
    assert (
        generate_diff(
            "tests/fixtures/flat_before.json", "tests/fixtures/flat_after.json"
        )
        == diff
    )


def test_flat_yaml_diff():
    with open("tests/fixtures/flat_diff.txt") as f:
        diff = f.read()
    assert (
        generate_diff(
            "tests/fixtures/flat_before.yaml", "tests/fixtures/flat_after.yaml"
        )
        == diff
    )
