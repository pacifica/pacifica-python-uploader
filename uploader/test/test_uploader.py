#!/usr/bin/python
"""Test the uploader module."""
from __future__ import absolute_import
from os import unlink
from time import sleep
from unittest import TestCase
from tempfile import NamedTemporaryFile
from .. import Uploader
from .. import bundler
from ..bundler.test.test_bundler import BuildSampleData
from ..metadata import MetaData, MetaObj


class TestUploader(TestCase):
    """Test the uploader class."""

    def test_uploader_module(self):
        """Test the uploader stuff."""
        self.assertTrue(Uploader)

    def test_uploader(self):
        """Test the uploader class."""
        up_obj = Uploader()
        self.assertTrue(up_obj)

    def test_upload_basic(self):
        """Test a basic minimal upload."""
        with BuildSampleData() as sample_files:
            md_obj = MetaData(
                [
                    MetaObj(destinationTable='Transactions._id', value=1234),
                    MetaObj(destinationTable='Transactions.submitter', value=10),
                    MetaObj(destinationTable='Transactions.proposal', value=u'1234a'),
                    MetaObj(destinationTable='Transactions.instrument', value=54)
                ]
            )
            bundle_fd = NamedTemporaryFile(delete=False)
            bundle = bundler.Bundler(md_obj, sample_files)
            bundle.stream(bundle_fd)
            bundle_fd.close()
            up_obj = Uploader()
            rbundle_fd = open(bundle_fd.name, 'r')
            job_id = up_obj.upload(rbundle_fd)
            self.assertTrue(job_id)
            status = up_obj.getstate(job_id)

            def check(status):
                """Check the status since it's complicated."""
                check = status['state'] != 'OK'
                check |= status['task'] != 'ingest metadata'
                check |= int(float(status['task_percent'])) != 100
                return check
            while check(status):
                sleep(1)
                status = up_obj.getstate(job_id)
            unlink(bundle_fd.name)
            self.assertTrue(status)
            self.assertEqual(status['state'], 'OK')
