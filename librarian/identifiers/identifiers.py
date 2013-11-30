"""
    Abstract class for an identification handler.
    Requires a filename on object creation.
    Requires an _identify and  cleanup method.
"""
from librarian.constants import WORKSPACE_PATH, OMDB_API_URL, LOGGING
from librarian.utils import md5_for_file
import logging.config
import requests

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class Identifier(object):

    def __init__(self, srcfile, path):
        self.srcfile = srcfile
        self.path = path

    def identify(self):
        """
            Generic method to identify files.
            Calls the get_title_meta function specified by each 
            base class to gather metadata
            Returns a list of JSON encoded objects for results
        """

        titles = self.get_titles()
        logger.debug("Found titles %s." % titles)
        metadata = self.get_title_metadata(titles)
        logger.debug("Metadata %s" % metadata)
        if not len(metadata):
            return None
        return metadata

    def get_titles(self):
        """
            Abstract method which returns a list of titles 
            for a given srcfile or returns None if no titles
            are found. Implemented by each subclass
        """
        raise NotImplementedError

    def get_title_metadata(self, titles):
        """
            Abstract method to gather metadata
            title: a list of titles to query
            returns: a JSON encoded list of results
        """
        raise NotImplementedError

class MovieIdentifier(Identifier):

    def get_title_metadata(self, titles):
        """
            Calls the OMDB API for each titles 
            and returns a list of results for matches
        """
        res = []
        for title in titles:
            r = requests.get(OMDB_API_URL, params={
                't': title,
            }).json()

            if r['Response']:
                res.append(r)
        return res


class HashIdentifier(Identifier):

    def __init__(self, srcfile, path, md5=None):
        super(MovieIdentifier, self).__init__(srcfile, path)
        if md5 is None:
            md5 = md5_for_file(self.srcfile)
        self.md5 = md5


    def get_titles(self):
        logger.debug("MD5 hash %s for %s" % (self.md5, self.srcfile))
        #TODO query metastore for match for hash
        return self.md5

    def get_title_metadata(self, titles):
        #TODO, call metastore for any matches found
        raise NotImplementedError

class TitleIdentifier(Identifier):

    def get_titles(self):
        raise NotImplementedError

    def get_title_metadata(self, titles):
        #TODO, call metastore for anymatches found
        raise NotImplementedError