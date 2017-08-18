#!/usr/bin/python
"""Test the metadata module."""
from unittest import TestCase
import metadata


class TestModule(TestCase):
    """Test the module for appropriate imports."""

    def test_module(self):
        """Test the metadata module for interface."""
        self.assertTrue(metadata.MetaData)
        self.assertTrue(metadata.MetaObj)
        self.assertTrue(metadata.metadata_encode)
        self.assertTrue(metadata.metadata_decode)
        self.assertTrue(metadata.FileObj)
