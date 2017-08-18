#!/usr/bin/python
"""This is the module for quering the Policy service."""
from os import getenv
import json
from collections import namedtuple
import requests
from metadata.Json import generate_namedtuple_encoder, generate_namedtuple_decoder, strip_obj

QUERY_KEYS = [
    'user',
    'columns',
    'from_table',
    'where'
]
PolicyQueryData = namedtuple('PolicyQueryData', QUERY_KEYS)
# Set the defaults to None for these attributes
PolicyQueryData.__new__.__defaults__ = (None,) * len(PolicyQueryData._fields)


class PolicyQuery(object):
    """
    Handle quering the policy server.

    This class handles quering the policy server and parsing the
    results.
    """

    pq_data = None
    user_id = None
    _addr = None
    _port = None
    _path = None
    _url = None
    _auth = None

    def set_user(self, user):
        """Set the user for the current PolicyQuery."""
        try:
            self.user_id = int(user)
        except ValueError:
            id_check = PolicyQuery(user=-1, columns=['_id'], from_table='users', where={'network_id': user})
            self.user_id = id_check.get_results()[0]['_id']

    def get_user(self):
        """Get the user id."""
        return self.user_id

    def _set_server_url(self, kwargs):
        """Set server url parts from kwargs or ENV if they aren't set."""
        parts = [
            ('port', 8181),
            ('addr', '127.0.0.1'),
            ('path', '/uploader'),
            ('url', None)
        ]
        for part, default in parts:
            attr_name = '_{}'.format(part)
            setattr(self, attr_name, kwargs.get(part))
            if not getattr(self, attr_name):
                setattr(self, attr_name, getenv('POLICY{}'.format(attr_name.upper()), default))
        if not self._url:
            self._url = 'http://{}:{}{}'.format(self._addr, self._port, self._path)

    def __init__(self, user, *args, **kwargs):
        """Set the policy server url and define any data for the query."""
        self._set_server_url(kwargs)
        self._auth = kwargs.get('auth', {})
        # global sential value for userid
        if user != -1:
            self.set_user(user)
            self.pq_data = PolicyQueryData(user=self.get_user(), *args, **kwargs)
        else:
            self.pq_data = PolicyQueryData(user=-1, **kwargs)

    def tojson(self):
        """Export self to json."""
        return json.dumps(self.pq_data, cls=PolicyQueryDataEncoder)

    @staticmethod
    def fromjson(json_str):
        """Import json string to self."""
        pq_data = json.loads(json_str, cls=PolicyQueryDataDecoder)
        pq_dict = pq_data._asdict()
        user = pq_dict.pop('user', -1)
        return PolicyQuery(user, **pq_dict)

    def get_results(self):
        """Get results from the Policy server for the query."""
        headers = {'content-type': 'application/json'}
        print self.tojson()
        reply = requests.post(self._url, headers=headers, data=self.tojson(), **self._auth)
        return json.loads(reply.content)


#####################################################################
# The from key in the json data is for the policy server.
# It's also a keyword in python so it needs to be handled correctly
#####################################################################
def _mangle_encode(obj):
    """Move the from_table to just from."""
    obj['from'] = obj.pop('from_table')
    strip_obj(obj)


def _mangle_decode(**json_data):
    """Mangle the decode of the policy query object."""
    json_data['from_table'] = json_data.pop('from')
    return PolicyQueryData(**json_data)


PolicyQueryDataEncoder = generate_namedtuple_encoder(PolicyQueryData, _mangle_encode)
PolicyQueryDataDecoder = generate_namedtuple_decoder(_mangle_decode)
