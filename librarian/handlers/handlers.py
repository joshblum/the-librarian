"""
    Abstract class for an entity handler.
    Subclasses by different entity types,
    used to call various identifiers on the entity
    and update the job progress in the system.
    Responsible for adding data to the metastore
    if an entity is identified.
"""
from librarian.constants import WORKSPACE_PATH, LOGGING, VIDEO_EXT
from librarian.utils import md5_for_file
from librarian.identifiers.identifiers import HashIdentifier, TitleIdentifier
from librarian.identifiers.movies.credits.identifier import MovieCreditIdentifier
# from librarian.identifiers.movies.fingerprint.identifier import AudioFingerprintIdentifier

import logging.config

import os
import uuid
import shutil
import glob

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

        self.srcfile = self.set_srcfile()
        self.init_job()

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
            #self.md5 = self.get_content_hash()
            # self.path = self.create_workspace()
            # insert job_id, md5, path into datastore
        raise NotImplementedError

    def finish_job(self, metadata):
        """
            Close the job out and add the metadata
            to the metastore
        """
        #TODO
        raise NotImplementedError

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

    def add_entity_metadata(self, metadata):
        """
            Add the metadata to the datastore
        """
        # TODO
        raise NotImplementedError

    def update_progress(self, status, msg=""):
        """
            Update the status of the current job
            Optionally add a status message.
        """
        # TODO
        raise NotImplementedError

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

    def __init__(self, srcpath, cleanup=True):
        super(Handler, self).__init__(srcpath, cleanup)

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
            identifier = identifier(*args)
            metadata = identifier.identify()
            logger.DEBUG("Running identifier %s, found metadata %s", % (identifier, metadata))
            #TODO update progress?
            if metadata is not None:
                return metadata

        return None
