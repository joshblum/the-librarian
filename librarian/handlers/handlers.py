"""
    Abstract class for an entity handler.
    Subclasses by different entity types,
    used to call various identifiers on the entity
    and update the job progress in the system.
    Responsible for adding data to the metastore
    if an entity is identified.
"""
from librarian.constants import WORKSPACE_PATH, LOGGING
from librarian.utils import md5_for_file
import logging.config

import os
import uuid
import shutil

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class Handler(object):

    def __init__(self, srcpath, cleanup=True):
        """
            Each subclass must call init_job in their __init__
            method and return the job_id that is set
        """
        self.srcpath = srcpath
        self.cleanup = cleanup

        # set by init_job
        self.path = None
        self.job_id = None

        # subclasses must set this attribute
        self.srcfile = None

    def create_workspace(self):
        """
            create a directory and return the absolute path
        """

        if not os.path.exists(WORKSPACE_PATH):
            os.mkdir(WORKSPACE_PATH)

        path = os.path.join(WORKSPACE_PATH, self.job_id)
        if not os.path.exists(path)
            os.mkdir(path)

        return path

    def cleanup_workspace(self):
        """
            Clear the tmp workspace if required
        """
        if self.cleanup:
            logger.debug("Removing dir %s", self.path)
            shutil.rmtree(self.path)

    def update_progress(self, status, msg=""):
        """
            Update the status of the current job
            Optionally add a status message.
        """
        # TODO
        raise NotImplementedError

    def init_job(self, srcfile):
        """
            Initialize and insert the job into the metastore.
            Adds job_id, path, and contents hash.
            Used by subclasses after self.srcfile is set.
            returns the job_id for the job
        """
        # TODO
        # if self.srcpath in datastore:
            # self.job_id = old_id
            # self.path = self.create_workspace()
        # else:
            # self.job_id = str(uuid.uuid4())
            #content_hash = self.get_content_hash()
            # self.path = self.create_workspace()
            #insert job_id, content_hash, path into datastore
        raise NotImplementedError

    def add_entity_metadata(self):
        """
            Abstract method to add metadata to the datastore
        """
        raise NotImplementedError

    def get_entity_metadata(self):
        """
            Abstract method to build Identifer class objects 
            to identify the entity and return the associated metadata
        """
        raise NotImplementedError

    def get_content_hash(self):
        """
            Returns the hash of self.srcfile
            Raises an Exception if self.srcfile is None
            This attribute must be set by subclasses
        """
        if self.srcfile is None:
            raise Exception("self.srcfile must not be None")

        return md5_for_file(self.srcfile)
