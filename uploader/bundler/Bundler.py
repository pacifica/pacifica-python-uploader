#!/usr/bin/python
"""Main Bundler module containing classes and methods to handle bundling."""
from os import path
from StringIO import StringIO
import threading
from time import sleep
import hashlib
from tarfile import TarFile, TarInfo
from datetime import datetime
from mimetypes import guess_type
from ..metadata import FileObj, metadata_encode


class HashFileObj(object):
    """File like object used for reading and hashing files."""

    def __init__(self, filedesc, hashval, upref):
        """Create the hash file object."""
        self.filedesc = filedesc
        self.hashval = hashval
        self.upref = upref

    def read(self, size=-1):
        """Read wrapper function."""
        buf = self.filedesc.read(size)
        self.hashval.update(buf)
        self.upref._done_size += len(buf)
        return buf

    def hashdigest(self):
        """Return the hash digest for the file."""
        return self.hashval.hexdigest()


# pylint: disable=too-few-public-methods
class Bundler(object):
    """Class to handle bundling of files to stream a tarfile."""

    md_obj = None
    file_data = None

    def __init__(self, md_obj, file_data, **kwargs):
        """
        Constructor of the bundler class.

        Add the MetaData object `md_obj` and file `file_data` to create.
        The `file_data` object should be a list of hashes.
        ```
        [
            {
                'name': 'local file path',
                'arcname': 'file path in the bundle',
                'recursive': 'True or False for directories'
            },
        ...
        ]
        ```
        """
        if not md_obj.is_valid():
            raise ValueError('MetaData is not valid yet.')
        self.md_obj = md_obj
        self.file_data = file_data
        hashstr = str(kwargs.get('hashfunc', 'sha1'))
        if hashstr not in hashlib.algorithms_available:
            raise ValueError('{} is not a valid hashlib algorithm.'.format(hashstr))
        self._hashfunc = getattr(hashlib, hashstr)
        self._hashstr = hashstr
        self._done_size = 0
        self._complete = False
        self._total_size = 0

    def _save_total_size(self):
        """Build the total size from the files and save the total."""
        tsize = 0
        for file_data in self.file_data:
            tsize += path.getsize(file_data['name'])
        self._total_size = tsize

    def _setup_notify_thread(self, callback, sleeptime=5):
        """Setup a notification thread calling callback with percent complete."""
        def notify():
            """Notify the callback with percent done while not complete."""
            while not self._complete:
                sleep(sleeptime)
                callback(float(self._done_size)/self._total_size)
        notifythread = threading.Thread(target=notify)
        notifythread.daemon = True
        notifythread.start()
        return notifythread

    @staticmethod
    def _strip_subdir(fname):
        """Remove the data subdir from the file path."""
        parts = fname.split('/')  # this is posix tar standard
        if parts[0] == 'data':
            del parts[0]
        parts = [x for x in parts if x]
        return '/'.join(parts)  # this is also posix tar standard

    def _build_file_info(self, file_data, hashsum):
        """Build the FileObj to and return it."""
        file_path = file_data['name']
        arc_path = file_data['arcname']
        mime_type = guess_type(file_path, strict=True)[0]
        info = {
            'size': path.getsize(file_path),
            'mimetype': mime_type if mime_type is not None else 'application/octet-stream',
            'name': path.basename(arc_path),
            'mtime': datetime.utcfromtimestamp(int(path.getmtime(file_path))).isoformat(),
            'ctime': datetime.utcfromtimestamp(int(path.getctime(file_path))).isoformat(),
            'destinationTable': 'Files',
            'subdir': self._strip_subdir(path.dirname(arc_path)),
            'hashtype': self._hashstr,
            'hashsum': hashsum
        }
        return FileObj(**info)

    def stream(self, fileobj, callback=None, sleeptime=5):
        """
        Stream the bundle to the fileobj.

        The fileobj should be an open file like object with 'wb' options.
        If the callback is given then percent complete of the size
        of the bundle will be given to the callback as the first argument.
        """
        notifythread = None
        if callable(callback):
            self._save_total_size()
            notifythread = self._setup_notify_thread(callback, sleeptime)

        tarfile = TarFile(None, 'w', fileobj)
        for file_data in self.file_data:
            tarinfo = tarfile.gettarinfo(**file_data)
            fileobj = HashFileObj(file_data.get('fileobj', open(file_data['name'])), self._hashfunc(), self)
            tarfile.addfile(tarinfo, fileobj)
            self.md_obj.append(self._build_file_info(file_data, fileobj.hashdigest()))
        md_txt = metadata_encode(self.md_obj)
        md_fd = StringIO(md_txt)
        md_tinfo = TarInfo('metadata.txt')
        md_tinfo.size = len(md_txt)
        tarfile.addfile(md_tinfo, md_fd)
        tarfile.close()
        self._complete = True

        if callable(callback):
            notifythread.join()
# pylint: enable=too-few-public-methods
