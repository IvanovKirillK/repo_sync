from tasks import check_file_exists
import pytest


def test_check_file_exists_case():
    assert check_file_exists('example/config.json') is True


def test_check_file_does_not_exists_case():
    assert check_file_exists('.\\test.json') is False


def test_check_file_does_not_exists_case_2():
    assert check_file_exists('123') is False


def test_check_empty_filename_case():
    with pytest.raises(TypeError):
        check_file_exists()