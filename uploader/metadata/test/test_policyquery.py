#!/usr/bin/python
"""Test the metadata module."""
from __future__ import absolute_import
from unittest import TestCase
from ..PolicyQuery import PolicyQuery


class TestPolicyQuery(TestCase):
    """Test the PolicyQuery service."""

    def test_pq_init(self):
        """Test the constructor for PolicyQuery."""
        policyquery = PolicyQuery('dmlb2001')
        self.assertTrue(policyquery)

    def test_pq_json(self):
        """Test converting the PolicyQuery to json."""
        policyquery = PolicyQuery('dmlb2001')
        self.assertEqual(policyquery.tojson(), '{"user": 10}')

    def test_pq_fromjson(self):
        """Test JSON to the PolicyQuery object."""
        policyquery = PolicyQuery.fromjson('{ "user": "dmlb2001", "from": "mytable" }')
        self.assertEqual(policyquery.pq_data.from_table, 'mytable')

    def test_pq_query(self):
        """Test JSON to the PolicyQuery object."""
        policyquery = PolicyQuery(
            user=-1,
            from_table='users',
            where={'network_id': 'dmlb2001'},
            columns=['last_name', 'first_name']
        )
        result = policyquery.get_results()
        self.assertEqual(result[0]['last_name'], u'Brown\u00e9 Jr')

    def test_get_user(self):
        """Test getting a user and converting it to and from ID/networkID."""
        policyquery = PolicyQuery(user=10)
        self.assertEqual(policyquery.get_user(), 10)
