#!/usr/bin/python
"""Encode and decode objects into json."""
import json


def strip_obj(obj):
    """Remove all keys who's values are False."""
    [obj.pop(x) for x in obj.keys() if not obj[x]]  # pylint: disable=expression-not-assigned


def generate_namedtuple_encoder(cls, mangle=strip_obj):
    """Return a namedtuple encoder for class cls."""
    class NamedTupleEncoder(json.JSONEncoder):
        """Class to encode a cls into json."""

        def encode(self, o):
            """Encode the cls into a json hash."""
            if isinstance(o, cls):
                obj = o._asdict()
                mangle(obj)
                return json.dumps(obj)
            return json.JSONEncoder.default(self, o)
    return NamedTupleEncoder


def generate_namedtuple_decoder(cls):
    """Return a namedtuple decoder for the class cls."""
    class NamedTupleDecoder(json.JSONDecoder):
        """Class to decode a json string into a cls object."""

        # pylint: disable=arguments-differ
        def decode(self, s):
            """Decode the string into a MetaObj object."""
            json_data = json.loads(s)
            if isinstance(json_data, dict):
                return cls(**json_data)
            raise TypeError('Unable to turn {} into a dict'.format(s))
        # pylint: enable=arguments-differ
    return NamedTupleDecoder
