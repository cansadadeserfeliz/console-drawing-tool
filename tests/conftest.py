import pytest

from drawing import Canvas


@pytest.fixture
def canvas():
    return Canvas('C 20 4')
