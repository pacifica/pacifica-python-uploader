#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This is the metadata library."""
from .metadata import MetaData, MetaObj, metadata_encode, metadata_decode, FileObj
from .metaupdate import MetaUpdate

__all__ = [
    'MetaData',
    'MetaObj',
    'FileObj',
    'MetaUpdate',
    'metadata_encode',
    'metadata_decode'
]
