#!/usr/bin/python
"""Test the metadata module."""
from metadata import MetaData, MetaObj, metadata_encode, metadata_decode


def test_reference_config():
    """Test the metadata module for interface."""
    metadata_str = open('test_data/up-metadata.json').read()
    metadata = metadata_decode(metadata_str)
    assert isinstance(metadata, MetaData)


def test_reference_upload_config():
    """Test the uploaded metadata to see if we can parse that."""
    metadata_str = open('test_data/good-md.json').read()
    metadata = metadata_decode(metadata_str)
    assert isinstance(metadata, MetaData)


def test_encoding():
    """Test the metadata encoding with simple example."""
    md_obj = MetaData([MetaObj(destinationTable='blarg')])
    meta_str = metadata_encode(md_obj)
    assert meta_str == '[{"destinationTable": "blarg"}]'


def test_error_md_encoding():
    """Fail to parse a MetaData object."""
    hit_exception = False
    try:
        metadata_encode(complex('1+2j'))
    except TypeError:
        hit_exception = True
    assert hit_exception


def test_error_mo_encoding():
    """Fail to parse a MetaData object."""
    hit_exception = False
    try:
        metadata_encode(MetaData([complex('1+2j')]))
    except TypeError:
        hit_exception = True
    assert hit_exception


def test_error_md_decoding():
    """Fail to parse a MetaData object."""
    hit_exception = False
    try:
        metadata_decode('{}')
    except TypeError:
        hit_exception = True
    assert hit_exception


def test_error_mo_decoding():
    """Fail to parse a MetaData object."""
    hit_exception = False
    try:
        metadata_decode('["blarg"]')
    except TypeError:
        hit_exception = True
    assert hit_exception
