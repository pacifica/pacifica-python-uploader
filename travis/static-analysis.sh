#!/bin/bash
pylint --rcfile=pylintrc uploader bundler metadata
pylint --rcfile=pylintrc setup.py
radon cc uploader bundler metadata
