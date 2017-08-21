#!/usr/bin/python
"""Setup and install the metadata."""
from pip.req import parse_requirements
from setuptools import setup

# parse_requirements() returns generator of pip.req.InstallRequirement objects
INSTALL_REQS = parse_requirements('requirements.txt', session='hack')

setup(name='PacificaUploader',
      version='1.0',
      description='Pacifica Uploader',
      author='David Brown',
      author_email='david.brown@pnnl.gov',
      packages=['bundler', 'uploader', 'metadata', 'common'],
      install_requires=[str(ir.req) for ir in INSTALL_REQS])
