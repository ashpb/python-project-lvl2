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


def test_json_diff():
    with open("tests/fixtures/diff.txt") as f:
        diff = f.read()
    assert (
        generate_diff(
            "tests/fixtures/before.json", "tests/fixtures/after.json"
        )
        == diff
    )


def test_yaml_diff():
    with open("tests/fixtures/diff.txt") as f:
        diff = f.read()
    assert (
        generate_diff(
            "tests/fixtures/before.yaml", "tests/fixtures/after.yaml"
        )
        == diff
    )


def test_json_diff2():
    with open("tests/fixtures/diff2.txt") as f:
        diff = f.read()
    assert (
        generate_diff(
            "tests/fixtures/before2.json", "tests/fixtures/after2.json"
        )
        == diff
    )


def test_yaml_diff2():
    with open("tests/fixtures/diff2.txt") as f:
        diff = f.read()
    assert (
        generate_diff(
            "tests/fixtures/before2.yaml", "tests/fixtures/after2.yaml"
        )
        == diff
    )
