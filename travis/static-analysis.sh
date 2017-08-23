#!/bin/bash
pre-commit run --all-files
pylint --rcfile=pylintrc pacifica/uploader *.py
radon cc pacifica/uploader *.py
