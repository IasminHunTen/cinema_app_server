import pytest

from main.utils.utils import *


@pytest.fixture
def req_response():
    return {'message': 'message'}, 17


def test_str_iter():
    assert not str_inter(
        [2*it for it in range(10)],
        [2*it + 1 for it in range(10)]
    )
    assert str_inter(
        [it for it in range(10)],
        [it for it in range(5, 15)]
    ) == 5


def test_doc_resp(req_response):
    assert doc_resp(req_response) == 17, 'message'

