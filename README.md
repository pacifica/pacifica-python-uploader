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
with other python objects. Additions to the `list` methods have been made to index off
the `metaID` attribute in the `MetaObj` class.

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

### Json

The `Json` module encapsulates the JSON parsing logic into a common library.
This module contains the general generators for creating `json.Encoder` and
`json.Decoder` child classes.

#### NamedTuple Encoders and Decoders

The `generate_namedtuple_encoder` and `generate_namedtuple_decoder` methods
return `json.Encoder` and `json.Decoder` child classes, respectively. These
classes encode or decode a child class of `collections.namedtuple`.

### Policy

This module contains all the logic to generate and execute queiries against
the Pacifica Policy service.

#### PolicyQueryData

This `namedtuple` contains the data required to generate a valid Policy
service query.

#### PolicyQuery

This object contains a `PolicyQueryData` object, mangles the object to send
it to the Policy service. This object also has logic to pull the endpoint for
the Policy service from the environment or constructor keyword arguments.
Another requirement for this object is to return the results from a query to
the calling object.

### MetaUpdate

This module has all the `MetaData` update code for determining parents and
children to update when values get updated.

#### MetaUpdate

The `MetaUpdate` class inherits from the `MetaData` class and provides methods
for querying the policy server to get results from the metadata and update
those results in the `MetaData` object.

## Bundler

This module defines a streaming bundler that allows one to stream the data and
metadata to a file descriptor. The file descriptor is open for write binary
and provides a single pass over the data files provided.

### Bundler

The `Bundler` class provides a method called `stream()` to send the bundle to
a file descriptor. The class is created using an array of hashes that define
the arguments to `tarfile.TarFile.gettarinfo()`. However, the `arcname` argument
is required. The `stream()` method is blocking. However, it does have a callback
argument that sets up a thread to get percent complete from the stream thread
as it's processing.

## Uploader

This module provides the basic upload functionality to interface with the
ingest service.

### Uploader

The `Uploader` class provides the interface for handling connections to the
ingest service. There are two methods `upload()` and `getstate()`. The
`upload()` method takes a file like object open for read binary and returns
a job_id for that upload. The `getstate()` method takes a job_id and returns
a json object as defined by the ingest API for getting job status.
