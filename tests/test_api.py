import pytest
from lexibot.api import Lexibot

def test_id(testbot):
   assert testbot.id.startswith('hayniecolorterms')


def test_python(testbot):
   assert testbot.python.stem == 'python3'
   assert testbot.python.is_absolute()


def test_error_on_missingdir(datadir):
    with pytest.raises(IOError):
        Lexibot(datadir / 'xx')
