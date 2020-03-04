# coding=utf-8
from pathlib import Path


def is_cldf_dataset(dirname):
    """Does the given directory contain a lexibank dataset?"""
    return True if list(Path(dirname).glob('*/*-metadata.json')) else False


def list_datadirs(dirname):
    for d in Path(dirname).iterdir():
        if d.is_dir() and is_cldf_dataset(d):
            yield d