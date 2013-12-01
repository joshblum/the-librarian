"""
    Abstract class for an entity handler.
    Subclasses by different entity types,
    used to call various identifiers on the entity
    and update the job progress in the system.
    Responsible for adding data to the metastore
    if an entity is identified.
"""
from librarian.constants import WORKSPACE_PATH, LOGGING, VIDEO_EXT, JOB_ENQUEUED, JOB_STARTED, JOB_INPROGRESS, JOB_FAILED, JOB_COMPLETED
from librarian.utils import md5_for_file
from librarian.identifiers.identifiers import HashIdentifier, TitleIdentifier
from librarian.identifiers.movies.credits.identifier import MovieCreditIdentifier
# from librarian.identifiers.movies.fingerprint.identifier import AudioFingerprintIdentifier
from librarian.metastore import MetaCon

import logging.config

import os
import uuid
import shutil
import glob

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class Handler(object):

    def __init__(self, job_id, srcpath,
                 entity_type, cleanup=True):
        """
            Each subclass must call init_job in their __init__
            method and return the job_id that is set
        """
        self.job_id = job_id
        self.srcpath = srcpath
        self.entity_type = entity_type
        self.cleanup = cleanup
        self.metastore = MetaCon()
        self.srcfile = self.set_srcfile()
        self.init_job()

    def init_job(self):
        """
            Initialize and insert the job into the metastore.
            Adds job_id, path, and contents hash.
            Used by subclasses after self.srcfile is set.
        """
        self.path = self.create_workspace()
        self.md5 = self.get_content_hash()

        logger.debug("Updating job %s" % self.job_id)

        self.metastore.update_job(
            self.job_id, srcpath=self.srcpath, md5=self.md5,
            progress=JOB_STARTED)

    def run(self):
        """
            Run the handler.
        """
        self.update_progress(JOB_INPROGRESS)

        progress = JOB_COMPLETED
        status = ""

        try:
            metadata = self.get_entity_metadata()
            logger.debug("Job %s Found metadata %s" % (
                self.job_id, metadata))
        except Exception, e:
            e = str(e)
            
            logger.debug("Job failed %s, %s" % (self.job_id, e))
            progress = JOB_FAILED
            status = e
            
            metadata = None

        if metadata is None:
            status += "\nUnble to identify."

        self.finish_job(metadata, progress, status)

    def finish_job(self, metadata, progress, status):
        """
            Close the job out and add the metadata
            to the metastore
        """
        # TODO update dstpath
        logger.debug("Job %s updating metadata %s" % (
                self.job_id, metadata))
        self.metastore.update_job(self.job_id, dstpath="",
                                  progress=progress, status=status)
        
        logger.debug("Adding %s metadata" % metadata)
        self.add_entity_metadata(metadata)
        self.cleanup_workspace()

    def create_workspace(self):
        """
            create a directory and return the absolute path
        """

        if not os.path.exists(WORKSPACE_PATH):
            os.mkdir(WORKSPACE_PATH)

        path = os.path.join(WORKSPACE_PATH, self.job_id)
        if not os.path.exists(path):
            os.mkdir(path)

        logger.debug("Created workspace %s" % path)

        return path

    def cleanup_workspace(self):
        """
            Clear the tmp workspace if required
        """
        if self.cleanup:
            logger.debug("Removing dir %s", self.path)
            shutil.rmtree(self.path)

    def add_entity_metadata(self, metadata):
        """
            Add the metadata to the datastore
        """
        if metadata is not None:
            metadata.update({
                'entity_type': self.entity_type,
                'job_id': self.job_id,
                'path': self.srcfile,
                'md5': self.md5,
            })
            self.metastore.add_entity_metadata(metadata)

    def update_progress(self, progress, status=""):
        """
            Update the status of the current job
            Optionally add a status message.
        """
        logger.debug("Updating job %s to progress %s" % (
            self.job_id, progress))
        self.metastore.update_job(self.job_id,
                                  progress=progress,
                                  status=status)

    def get_content_hash(self):
        """
            Returns the hash of self.srcfile
            self.srcfile is set by subclasses
        """

        return md5_for_file(self.srcfile)

    def set_srcfile(self):
        """
            Abstract method to determine what the srcfile
            is for a given entity handler
        """
        raise NotImplementedError

    def get_entity_metadata(self):
        """
            Abstract method to build Identifer class objects 
            to identify the entity and return the associated metadata
        """
        raise NotImplementedError


class MovieHandler(Handler):

    def __init__(self, job_id, srcpath, entity_type, cleanup=True):
        super(MovieHandler, self).__init__(
            job_id, srcpath, entity_type, cleanup)

    def set_srcfile(self):
        """
            Sets the srcfile attribute
            A single video file is used as the srcfile
            for a movie. If multiple movies are found,
            exception is raised.
            TODO: Join multiple files if found (i.e. movie split into two disks)
        """
        files = glob.glob("%s*" % self.srcpath)
        srcfiles = []
        for path in files:
            split_path = path.split(".")
            if len(split_path) and split_path[-1] in VIDEO_EXT:
                srcfiles.append(path)

        if len(srcfiles) == 1:
            return srcfiles[0]

        raise Exception("More than one possible srcfile for %s" % self.srcpath)

    def get_entity_metadata(self):
        """
            Tries to identify the srcfile with the following steps
            1. Simple hash
            2. Title matching #TODO
                2.1 srcpath
                2.2 srcfile
            3. Credit matching
            4. Audio fingerprinting #TODO
        """
        default_args = (self.srcfile, self.path)
        identifiers = [(HashIdentifier, (self.srcfile, self.path, self.md5)),
                       #(TitleIdentifier, (self.srcpath, self.path)),
                       #(TitleIdentifier, default_args),
                       (MovieCreditIdentifier, default_args),
                       #(AudioFingerprintIdentifier default_args),
                       ]
        for identifier, args in identifiers:
            status = "Running identifier %s, found metadata %s" % (
                identifier, metadata)
            logger.DEBUG(status)
            identifier = identifier(*args)
            metadata = identifier.identify()
            self.update_progress(JOB_INPROGRESS, status)

            if metadata is not None:
                return metadata

        return None


class DummyHandler(Handler):

    """
        Default handler if an entity does not have a valid type
        Fails the job and adds it to the metastore
    """

    def set_srcfile(self):
        return None

    def get_entity_metadata(self):
        return None
