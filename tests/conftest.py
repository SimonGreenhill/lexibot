# coding=utf-8
from pathlib import Path
from shutil import copytree
import pytest

from git import Repo

from lexibot import Lexibot

@pytest.fixture
def datadir():
    return Path(__file__).parent / 'testdata'


@pytest.fixture
def testbot(datadir):
    return Lexibot(datadir / 'hayniecolorterms')

