#!/usr/bin/python
"""Module used to update MetaData objects."""
from __future__ import absolute_import
from .MetaData import MetaData
from .PolicyQuery import PolicyQuery


class MetaUpdate(MetaData):
    """Class to update the MetaData object."""

    def __init__(self, user, *args, **kwargs):
        """Pull the user from the arguments so we can use that for policy queries."""
        self._auth = kwargs.pop('auth', {})
        super(MetaUpdate, self).__init__(*args, **kwargs)
        self._user = user

    def query_results(self, meta_id):
        """Build a PolicyQuery out of the meta_id."""
        where_clause = {}
        for column, dep_meta_id in self[meta_id].queryDependency.iteritems():
            where_clause[column] = self[dep_meta_id].value
        pq_obj = PolicyQuery(
            user=self._user,
            columns=self[meta_id].queryFields,
            from_table=self[meta_id].sourceTable,
            where=where_clause,
            auth=self._auth
        )
        return pq_obj.get_results()

    def update_parents(self, meta_id):
        """Update the parents of the meta_id."""
        meta = self[meta_id]
        for dep_meta_id in meta.queryDependency.values():
            if meta_id != dep_meta_id:
                self.update_parents(dep_meta_id)

        meta = meta._replace(query_results=self.query_results(meta_id))
        self[meta_id] = meta

        if not meta.value:
            meta = meta._replace(value=meta.query_results[0]['_id'])
            self[meta_id] = meta
