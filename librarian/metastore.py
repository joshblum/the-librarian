"""
    API for iteraction with main metastore
    Stores metadata with associated items and job progress
"""

from pymongo import MongoClient
from constants import DEFAULT_DB, DEFAULT_JOB_COLLECTION, DEFAULT_META_COLLECTION


class MongoCon():

    def __init__(self, db_name=DEFAULT_DB,
                 job_collection=DEFAULT_JOB_COLLECTION,
                 meta_collection=DEFAULT_META_COLLECTION):
        self.db_name = db_name
        self.db = self.connect(db_name)
        self.job_collection = self.get_collection(job_collection)
        self.meta_collection = self.get_collection(meta_collection)

    def connect(self, db_name):
        # must have mongo instance running
        connection = MongoClient()
        return connection[db_name]

    def get_collection(self, name):
        return self.db[name]

    def execute_query(self, query, collection):
        collection = self._assign_collection(collection)
        return collection.find(query)