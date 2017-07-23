#!/usr/bin/python
"""MetaData class to handle input and output of metadata format."""
import json
from collections import namedtuple


class MetaData(list):
    """Class to hold a list of MetaObj and FileObj objects."""

    pass


META_KEYS = [
    'sourceTable',
    'destinationTable',
    'metaID',
    'displayType',
    'displayTitle',
    'queryDependency',
    'valueField',
    'queryFields',
    'diplayFormat',
    'key',
    'value',
    'directoryOrder'
]
MetaObj = namedtuple('MetaObj', META_KEYS)
# Set the defaults to None for these attributes
MetaObj.__new__.__defaults__ = (None,) * len(MetaObj._fields)

FILE_KEYS = [
    'destinationTable',
    'name',
    'subdir',
    'size',
    'hashtype',
    'hashsum',
    'mimetype',
    'ctime',
    'mtime'
]
FileObj = namedtuple('FileObj', FILE_KEYS)
# Set the defaults to None for these attributes
FileObj.__new__.__defaults__ = (None,) * len(FileObj._fields)


class MetaObjEncoder(json.JSONEncoder):
    """Class to encode a MetaObj into json."""

    def encode(self, o):
        """Encode the MetaObj into a json hash."""
        if isinstance(o, MetaObj):
            obj = o._asdict()
            [obj.pop(x) for x in obj.keys() if not obj[x]]  # pylint: disable=expression-not-assigned
            return json.dumps(obj)
        return json.JSONEncoder.default(self, o)


class MetaDataEncoder(json.JSONEncoder):
    """Class to encode a MetaData object into json."""

    def encode(self, o):
        """Encode the MetaData object into a json list."""
        if isinstance(o, MetaData):
            json_parts = []
            for mobj in o:
                json_parts.append(json.loads(json.dumps(mobj, cls=MetaObjEncoder)))
            return json.dumps(json_parts)
        return json.JSONEncoder.default(self, o)


class MetaObjDecoder(json.JSONDecoder):
    """Class to decode a json string into a MetaObj object."""

    # pylint: disable=arguments-differ
    def decode(self, s):
        """Decode the string into a MetaObj object."""
        json_data = json.loads(s)
        if isinstance(json_data, dict):
            if json_data.get('destinationTable') == 'Files':
                return FileObj(**json_data)
            return MetaObj(**json_data)
        raise TypeError('Unable to turn {} into a dict'.format(s))
    # pylint: enable=arguments-differ


class MetaDataDecoder(json.JSONDecoder):
    """Class to decode a json string into a MetaData object."""

    # pylint: disable=arguments-differ
    def decode(self, s):
        """Decode the string into a MetaData object."""
        json_data = json.loads(s)
        if isinstance(json_data, list):
            return MetaData([MetaObjDecoder().decode(json.dumps(obj)) for obj in json_data])
        raise TypeError('Unable to turn {} into a list'.format(s))
    # pylint: enable=arguments-differ


def metadata_decode(json_str):
    """Decode the json string into MetaData object."""
    return json.loads(json_str, cls=MetaDataDecoder)


def metadata_encode(md_obj):
    """Encode the MetaData object into a json string."""
    return json.dumps(md_obj, cls=MetaDataEncoder)
