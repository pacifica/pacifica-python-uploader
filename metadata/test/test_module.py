#!/usr/bin/python
"""Test the metadata module."""
import metadata


def test_module():
    """Test the metadata module for interface."""
    assert metadata.MetaData
    assert metadata.MetaObj
    assert metadata.metadata_encode
    assert metadata.metadata_decode
