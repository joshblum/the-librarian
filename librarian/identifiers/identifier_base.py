"""
    Abstract class for an identification handler.
    Requires a filename on object creation.
    Requires an _identify and  cleanup method.
"""
from librarian.constants import WORKSPACE_PATH, OMDB_API_URL

import requests
import shutil
import uuid
import os


class Identifier(object):

    def __init__(self, srcfile, cleanup=False):
        self.srcfile = srcfile
        self.cleanup = cleanup
        self.path = self.create_workspace()

    def create_workspace(self):
        """
            create a directory and return the absolute path
        """

        dirname = str(uuid.uuid4())
        if not os.path.exists(WORKSPACE_PATH):
            os.mkdir(WORKSPACE_PATH)

        path = os.path.join(WORKSPACE_PATH, dirname)
        os.mkdir(path)
        return path

    def identify(self):
        """
            Generic method to identify files.
            Calls the get_title_meta function specified by each 
            base class to gather metadata
            Returns a list of JSON encoded objects for results
        """

        titles = self.find_titles()
        self.cleanup_workspace()
        return self.get_title_metadata(titles)

    def find_titles(self):
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

    def cleanup_workspace(self):
        """
            Clear the tmp workspace if required
        """
        if self.cleanup:
            shutil.rmtree(self.path)


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
