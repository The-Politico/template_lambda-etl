import os
from process import Process
from process.errors import MismatchedDataSchema


def test_bad_data():
    file_path = os.path.abspath("./test/data/bad.xlsx")
    dataset = Process(file_path)
    try:
        dataset.etl()
    except MismatchedDataSchema:
        assert True
        return
    assert False


def test_good_data():
    file_path = os.path.abspath("./test/data/good.xlsx")
    dataset = Process(file_path)
    try:
        dataset.etl()
    except Exception:
        assert False
        return
    assert True
