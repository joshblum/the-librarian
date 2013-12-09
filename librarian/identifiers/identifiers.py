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

    def __str__(self):
        return self.__class__.__name__

    def identify(self):
        """
            Generic method to identify files.
            Calls the get_title_meta function specified by each 
            base class to gather metadata
            Returns a dictionary of JSON encoded objects for results
        """

        titles = self.get_titles()
        logger.debug("Found titles %s." % titles)
        metadata = self.get_title_metadata(titles)
        logger.debug("Metadata %s" % metadata)
        if metadata is None or not len(metadata):
            return None
        return {
            'data': metadata,
        }

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
    metadata_map = {
        'Actors': 'actors',
        'BoxOffice': 'box_office',
        'DVD': 'dvd',
        'Director': 'director',
        'Genre': 'genre',
        'Plot': 'plot',
        'Poster': 'poster',
        'Production': 'production',
        'Rated': 'rated',
        'Released': 'released',
        'Runtime': 'runtime',
        'Title': 'title',
        'Type': 'type',
        'Website': 'website',
        'Writer': 'writer',
        'Year': 'year',
        'imdbID': 'imdb_id',
        'imdbRating': 'imdb_rating',
        'imdbVotes': 'imdb_votes',
        'tomatoConsensus': 'tomato_consensus',
        'tomatoFresh': 'tomato_fresh',
        'tomatoImage': 'tomato_image',
        'tomatoMeter': 'tomato_meter',
        'tomatoRating': 'tomato_rating',
        'tomatoReviews': 'tomato_reviews',
        'tomatoRotten': 'tomato_rotten',
        'tomatoUserMeter': 'tomato_user_meter',
        'tomatoUserRating': 'tomato_user_rating',
        'tomatoUserReviews': 'tomato_user_reviews',
    }

    def get_title_metadata(self, titles):
        """
            Calls the OMDB API for each titles 
            and returns a list of results for matches
        """
        res = []
        for title in titles:
            params = self.get_params(title)
            r = requests.get(OMDB_API_URL, params=params).json()
            if r['Response']:
                res.append(self.clean_metadata(r))
        return res

    def get_params(self, title):
        return {
            't': title,
            'tomatoes': True,
        }

    def clean_metadata(self, metadata):
        """
            change the keys of the metadata dictionary to 
            the format we want
        """
        clean_meta = {}
        for key, clean_key in self.metadata_map.iteritems():
            clean_meta[clean_key] = metadata[key]
        return clean_meta


class HashIdentifier(Identifier):

    def __init__(self, srcfile, path, md5=None):
        super(HashIdentifier, self).__init__(srcfile, path)
        if md5 is None:
            md5 = md5_for_file(self.srcfile)
        self.md5 = md5

    def get_titles(self):
        logger.debug("Getting titles for %s" % self.srcfile)
        metadata = self.metastore.find_metadata_by_md5(self.md5)
        if metadata is None:
            return None
        return [item['title'] 
            for data in metadata['data'] 
                for item in data['data']]

    def get_title_metadata(self, titles):
        return self.metastore.find_metadata_by_md5(self.md5)
