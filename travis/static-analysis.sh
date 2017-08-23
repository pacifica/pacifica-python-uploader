#!/bin/bash
pre-commit run --all-files
pylint --rcfile=pylintrc uploader *.py
radon cc uploader *.py
