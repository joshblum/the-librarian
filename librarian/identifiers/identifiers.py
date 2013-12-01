"""
    Abstract class for an identification handler.
    Requires a filename on object creation.
    Requires an _identify and  cleanup method.
"""
from librarian.constants import WORKSPACE_PATH, OMDB_API_URL, LOGGING
from librarian.utils import md5_for_file
from librarian.metastore import MetaCon
import logging.config
import requests

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class Identifier(object):

    def __init__(self, srcfile, path):
        self.srcfile = srcfile
        self.path = path
        self.metastore = MetaCon()

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
    metadata_keys = set([
        'actors',
        'box_office',
        'dvd',
        'director',
        'genre',
        'plot',
        'poster',
        'production',
        'rated',
        'released',
        'runtime',
        'title',
        'type',
        'website',
        'writer',
        'year',
        'imdb_id',
        'imdb_rating',
        'imdb_votes',
        'tomato_consensus',
        'tomato_fresh',
        'tomato_image',
        'tomato_meter',
        'tomato_rating',
        'tomato_reviews',
        'tomato_rotten',
        'tomato_user_meter',
        'tomato_user_rating',
        'tomato_user_reviews',
    ])

    def get_title_metadata(self, titles):
        """
            Calls the OMDB API for each titles 
            and returns a list of results for matches
        """
        res = []
        for title in titles:
            r = requests.get(OMDB_API_URL, params={
                't': title,
                'tomatoes': True,
            }).json()

            if r['Response']:
                res.append(self.clean_metadata(r))
        return res

    def clean_metadata(self, metadata):
        """
            change the keys of the metadata dictionary to 
            the format we want
        """
        clean = {}
        for key in self.metadata_keys:
            clean[key] = metadata[key]
        return clean


class HashIdentifier(Identifier):

    def __init__(self, srcfile, path, md5=None):
        super(HashIdentifier, self).__init__(srcfile, path)
        if md5 is None:
            md5 = md5_for_file(self.srcfile)
        self.md5 = md5

    def get_titles(self):
        logger.debug("Getting titles for %s" % self.srcfile)
        metadata = self.metastore.find_metadata_by_md5(self.md5)
        return [item['title'] for item in metadata]

    def get_title_metadata(self, titles):
        return list(self.metastore.find_metadata_by_md5(self.md5))

class TitleIdentifier(Identifier):

    def get_titles(self):
        raise NotImplementedError

    def get_title_metadata(self, titles):
        # TODO, call metastore for anymatches found
        raise NotImplementedError
