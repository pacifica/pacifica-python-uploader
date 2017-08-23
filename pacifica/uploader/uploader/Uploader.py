#!/usr/bin/python
"""Uploader module send the data to the ingest service."""
from pacifica.uploader.common import CommonBase


class Uploader(CommonBase):
    """Uploader class to upload the bundle to an ingest server."""

    _addr = None
    _port = None
    _upload_path = None
    _status_path = None
    _upload_url = None
    _status_url = None
    _auth = None

    def __init__(self, **kwargs):
        """Set the ingest endpoint url."""
        self._setup_requests_session()
        self._server_url(
            [
                ('port', 8066),
                ('addr', '127.0.0.1'),
                ('upload_path', '/upload'),
                ('status_path', '/get_state'),
                ('upload_url', None),
                ('status_url', None)
            ],
            'INGEST',
            kwargs
        )
        if not self._upload_url:
            self._upload_url = 'http://{}:{}{}'.format(self._addr, self._port, self._upload_path)
        if not self._status_url:
            self._status_url = 'http://{}:{}{}'.format(self._addr, self._port, self._status_path)
        self._auth = kwargs.get('auth', {})

    def upload(self, read_fd):
        """Upload the data from a file like object."""
        headers = {'content-type': 'application/octet-stream'}
        resp = self.session.post(self._upload_url, data=read_fd, headers=headers)
        return resp.json()['job_id']

    def getstate(self, job_id):
        """Get the ingest state for a job."""
        resp = self.session.get('{}?job_id={}'.format(self._status_url, job_id))
        return resp.json()
