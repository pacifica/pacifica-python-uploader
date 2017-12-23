#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Setup and install the metadata."""
from pip.req import parse_requirements
from setuptools import setup

# parse_requirements() returns generator of pip.req.InstallRequirement objects
INSTALL_REQS = parse_requirements('requirements.txt', session='hack')

setup(
    name='PacificaUploader',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description='Pacifica Uploader',
    author='David Brown',
    author_email='david.brown@pnnl.gov',
    packages=[
        'uploader',
        'uploader.bundler',
        'uploader.common',
        'uploader.metadata'
    ],
    install_requires=[str(ir.req) for ir in INSTALL_REQS]
)
