from tasks import check_dir_exists
import pytest


def test_check_dir_exists_case():
    assert check_dir_exists('example') is True


def test_check_dir_does_not_exists_case():
    assert check_dir_exists('nonexisting') is False


def test_check_dir_does_not_exists_case_2():
    assert check_dir_exists('123') is False


def test_check_empty_dir_case():
    with pytest.raises(TypeError):
        check_dir_exists()