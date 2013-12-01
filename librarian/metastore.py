"""
    API for iteraction with main metastore
    Stores metadata with associated items and job progress
"""

from pymongo import MongoClient, DESCENDING
from constants import DEFAULT_DB, DEFAULT_JOB_COLLECTION, DEFAULT_META_COLLECTION, JOB_ENQUEUED
from datetime import datetime

import bson


class MetaCon():

    def __init__(self, db_name=DEFAULT_DB,
                 job_collection=DEFAULT_JOB_COLLECTION,
                 meta_collection=DEFAULT_META_COLLECTION):
        self.db_name = db_name
        self.db = self.connect(db_name)
        self.job_collection = self.get_collection(job_collection)
        self.meta_collection = self.get_collection(meta_collection)
        self.add_job_index()
        self.add_meta_index()

    def connect(self, db_name):
        # must have mongo instance running
        connection = MongoClient()
        return connection[db_name]

    def get_collection(self, name):
        return self.db[name]

    def add_job_index(self):
        """
            Index the job table on srcpath and dstpath.
        """
        self.job_collection.create_index([("srcpath", DESCENDING)])
        self.job_collection.create_index([("dstpath", DESCENDING)])

    def add_meta_index(self):
        """
            Index the meta table on ?
        """
        # TODO
        pass

    def add_job(self, job_doc):
        """
            Insert a new job into the metastore
        """
        self.job_collection.insert(job_doc)

    def update_job(self, job_id, **kwargs):
        """
            Update a new job into the metastore
        """
        # valid kwargs
        fields = self.get_job_doc(None, None, None)
        for k in kwargs:
            assert k in fields

        md5 = 'md5'
        if md5 in kwargs:
            kwargs[md5] = bson.Binary(kwargs[md5])

        self.job_collection.update(
            {'job_id': job_id},
            {'$set': kwargs},
        )

    def find_job_by_id(self, job_id):
        return self.find_one(self.job_collection, {
            'job_id': job_id,
        })

    def find_enqueued_jobs(self):
        return self.find(self.job_collection, {
            'progress': JOB_ENQUEUED
        })

    def find_one(self, collection, query):
        return collection.find_one(query)

    def find(self, collection, query):
        return collection.find(query)

    def get_job_doc(self, job_id, entity_type, srcpath, dstpath=None,
                    md5=None, progress=JOB_ENQUEUED,
                    status="", timestamp=datetime.now()):
        """
            Util for creating a job type document.
        """
        return {
            'job_id': job_id,
            'entity_type': entity_type,
            'srcpath': srcpath,
            'dstpath': dstpath,
            'md5': md5,
            'progress': progress,
            'status': status,
            'timestamp': timestamp,
        }

    def add_entity_metadata(self, metadata):
        """
            metadata object for various entity types,
            required keys listed below. If these keys are not
            present assertion error is thrown.
        """
        required_keys = [
            'job_id',
            'entity_type',
            'path',
            'md5',
        ]
        for key in required_keys:
            assert key in metadata

        metadata['timestamp'] = datetime.now()
        self.meta_collection.insert(metadata)

    def find_metadata_by_md5(self, md5):
        return self.find(self.meta_collection, {
            'md5': bson.Binary(md5),
        })
