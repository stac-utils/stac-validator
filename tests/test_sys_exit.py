import subprocess

import pytest


def test_correct_sys_exit_error_python():
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.run(
            ["stac-validator", "tests/test_data/bad_data/bad_item_v090.json"],
            check=True,
        )


def test_correct_sys_exit_error_recursion():
    try:
        subprocess.run(
            [
                "stac_validator",
                "tests/test_data/v100/catalog-with-bad-item.json",
                "--recursive",
                "-1",
            ],
            check=True,
        )
        assert False
    except subprocess.CalledProcessError:
        assert True


def test_false_sys_exit_error_python():
    subprocess.run(
        ["stac-validator", "tests/test_data/v090/items/good_item_v090.json"],
        check=True,
    )
