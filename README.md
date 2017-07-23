# Pacifica Python Uploader
[![Build Status](https://travis-ci.org/pacifica/pacifica-python-uploader.svg?branch=master)](https://travis-ci.org/pacifica/pacifica-python-uploader)
[![Code Climate](https://codeclimate.com/github/pacifica/pacifica-python-uploader/badges/gpa.svg)](https://codeclimate.com/github/pacifica/pacifica-python-uploader)
[![Test Coverage](https://codeclimate.com/github/pacifica/pacifica-python-uploader/badges/coverage.svg)](https://codeclimate.com/github/pacifica/pacifica-python-uploader/coverage)
[![Issue Count](https://codeclimate.com/github/pacifica/pacifica-python-uploader/badges/issue_count.svg)](https://codeclimate.com/github/pacifica/pacifica-python-uploader)

Python library to handle bundling, metadata and uploading files to an ingester.

## MetaData

The `MetaData` module handles the required metadata needed to create a successful
upload. The logic for encoding and decoding into JSON is also present in the library.
This object must encode into JSON compatible with the ingest service.

### MetaData Object

The `MetaData()` object is the upperlevel object storing all the required upload and
file metadata. This object is currently a child of `list` to allow for easy integration
with other python objects.

### MetaObj Object

The `MetaObj()` object is an instance of a single piece of uploaded metadata. This
means that it's not file metadata. The `MetaObj()` object allows for references
between attributes of the class and allows for updates to occure at the `MetaData()`
layer. This is currently implemented as a `namedtuple` for easy integration with
other python objects.

### FileObj Object

The `FileObj()` object is an instance of a single files metadata. This is meant to
be appended to the `MetaData()` object when an upload occures. The attributes of the
`FileObj()` directly match with the file object stored in
[Pacifica Metadata](https://github.com/pacifica/pacifica-metadata)
so please refer to that for what the
values are supposed to be. This is currently implemented as a `namedtuple` for easy
integration with other python objects.

### Metadata Decode

The `metadata_decode()` method decodes a JSON string into a `MetaData()` object
filled with `MetaObj()` and `FileObj()` objects. The method returns the resulting
`MetaData()` object.

### Metadata Encoding

The `metadata_encode()` method encodes a `MetaData()` object with a number of
`MetaObj()` and `FileObj()` objects into a JSON string. The method returns the
resulting JSON string.
