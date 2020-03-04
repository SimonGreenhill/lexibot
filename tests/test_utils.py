import pytest
from lexibot.utils import is_cldf_dataset, list_datadirs

def test_is_cldf_dataset(datadir):
    assert is_cldf_dataset(datadir / "hayniecolorterms")
    assert not is_cldf_dataset(datadir / "not-a-dataset")


def test_list_datadirs(datadir):
    assert list([_.stem for _ in list_datadirs(datadir)]) == ['hayniecolorterms']
