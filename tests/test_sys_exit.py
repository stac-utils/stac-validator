import subprocess


def test_correct_sys_exit_error_python():
    try:
        subprocess.run(
            ["stac_validator", "tests/test_data/bad_data/bad_item_v090.json"],
            check=True,
        )
        assert False
    except subprocess.CalledProcessError:
        assert True


def test_false_sys_exit_error_python():
    try:
        subprocess.run(
            ["stac_validator", "tests/test_data/v090/items/good_item_v090.json"],
            check=True,
        )
        assert True
    except subprocess.CalledProcessError:
        assert False
