"""
    Abstract class for an entity handler.
    Subclasses by different entity types,
    used to call various identifiers on the entity
    and update the job progress in the system.
    Responsible for adding data to the metastore
    if an entity is identified.
"""
from librarian.constants import WORKSPACE_PATH, LOGGING,\
    VIDEO_EXT, JOB_ENQUEUED, JOB_STARTED, JOB_INPROGRESS, JOB_FAILED, JOB_COMPLETED, JOB_DUPLICATE
from librarian.utils import md5_for_file
from librarian.identifiers.identifiers import HashIdentifier
from librarian.identifiers.movies.credits.identifier import MovieCreditIdentifier
from librarian.identifiers.movies.title.identifier import MovieTitleIdentifier
from librarian.identifiers.movies.audio.identifier import MovieAudioIdentifier
from librarian.identifiers.movies.audio.extract_audio import fingerprint_for_file
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

        if self.srcfile is None:  # job failed
            return

        self.path = self.create_workspace()
        self.md5 = self.get_content_hash()
        self.fingerprint = None  # self.get_content_fingerprint()

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

        metadata = None
        meta_id = None
        try:
            meta_id = self.is_dup()
            if meta_id is not None:
                logger.debug("Job %s marked as duplicate" % self.job_id)
            else:
                metadata = self.get_entity_metadata()
                logger.debug("Job %s Found metadata %s" % (
                    self.job_id, metadata))
        except Exception, e:

            logger.exception("Job failed %s, %s" % (self.job_id, e))
            progress = JOB_FAILED
            status = str(e)

        if metadata is None and meta_id is not None:
            status += "\nUnable to identify."

        self.finish_job(meta_id, metadata, progress, status)

    def finish_job(self, meta_id, metadata, progress, status):
        """
            Close the job out and add the metadata
            to the metastore
        """
        # TODO update dstpath
        logger.debug("Adding %s metadata" % metadata)

        if meta_id is None:
            meta_id = self.add_entity_metadata(metadata)

        self.metastore.update_job(self.job_id, meta_id=meta_id,
                                  dstpath="", progress=progress,
                                  status=status)

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
        meta_id = None
        if metadata is not None:
            metadata = {
                'entity_type': self.entity_type,
                'md5': self.md5,
                'fingerprint': self.fingerprint,
                'data': metadata
            }
            logger.debug("Adding metadata %s" % metadata)
            meta_id = self.metastore.add_entity_metadata(metadata)
        return meta_id

    def update_progress(self, progress, **kwargs):
        """
            Update the status of the current job
            Optionally add a status message.
        """
        logger.debug("Updating job %s to progress %s" % (
            self.job_id, progress))
        kwargs['progress'] = progress
        self.metastore.update_job(self.job_id, **kwargs)

    def get_content_hash(self):
        """
            Returns the hash of self.srcfile
            self.srcfile is set by subclasses
        """

        return md5_for_file(self.srcfile)

    def get_content_fingerprint(self):
        """
            Returns the fingerprint of self.srcfile
            self.srcfile is set by subclasses
        """

        return fingerprint_for_file(self.path, self.srcfile)

    def is_dup(self):
        """
            Abstract method to check if the entity is a duplicate
            or not.
        """
        raise NotImplementedError

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
        if os.path.isdir(self.srcpath) and self.srcpath[-1] != os.sep:
            self.srcpath += os.sep

        files = glob.glob("%s*" % self.srcpath)
        srcfiles = []
        logger.debug("Found files %s" % files)
        for path in files:
            split_path = path.split(".")
            if len(split_path) and split_path[-1] in VIDEO_EXT:
                srcfiles.append(path)

        if len(srcfiles) == 1:
            return srcfiles[0]

        status = "Found srcs %s." % (srcfiles)
        self.update_progress(self.job_id, JOB_FAILED, status=status)
        return None

    def is_dup(self):
        """
            Checks audio fingerprint and simple hash for duplicates
        """
        default_args = (self.srcfile, self.path)
        dup_detectors = [(HashIdentifier, (self.srcfile, self.path, self.md5)),
                         #                     (MovieAudioIdentifier, default_args),
                         ]
        for detector, args in dup_detectors:
            logger.debug("Running dedup detector %s with args %s" %
                         (detector, args))

            detector = detector(*args)
            data = detector.identify()

            status = "Ran detector %s, found metadata %s" % (
                detector, data)

            logger.debug(status)

            if data is not None:
                meta_id = data['data']['_id']
                self.update_progress(JOB_DUPLICATE, status,
                                     meta_id=meta_id, src=str(detector))
                return meta_id

        return None

    def get_entity_metadata(self):
        """
            Tries to identify the srcfile with the following steps
            1. Title matching
                1.1 srcpath
                1.2 srcfile
            2. Credit matching
        """
        default_args = (self.srcfile, self.path)
        identifiers = [(MovieTitleIdentifier, (self.srcpath, self.path)),
                       (MovieTitleIdentifier, default_args),
                       (MovieCreditIdentifier, default_args),
                       ]
        metadata = []
        for identifier, args in identifiers:
            logger.debug("Running identifier %s with args %s" %
                         (identifier, args))
            identifier = identifier(*args)
            data = identifier.identify()
            status = "Ran identifier %s, found metadata %s" % (
                identifier, data)

            if data is not None:
                data['src'] = str(identifier)
                metadata.append(data)

            logger.debug(status)
            self.update_progress(JOB_INPROGRESS, status,
                                 src="identifier")

        return metadata


class DummyHandler(Handler):

    """
        Default handler if an entity does not have a valid type
        Fails the job and adds it to the metastore
    """

    def set_srcfile(self):
        return None

    def get_entity_metadata(self):
        return None
