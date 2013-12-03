"""
    Movie title identification handler.
    Create this object with a srcfile that contains the title
"""

from librarian.constants import LOGGING
from librarian.identifiers.identifiers import Identifier

import logging.config
import inspect
import os
import re

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class TitleIdentifier(Identifier):

    def __init__(self, srcfile, path):
        super(TitleIdentifier, self).__init__(srcfile, path)

        self.title = os.path.basename(srcfile)
        self.parsers = TitleParser(title)

    def get_titles(self):
        possible_titles = self.parser.parse()

        # TODO query film name db to weed out bad data
        return possible_titles

    def get_title_metadata(self, titles):
        # todo query OMDB/TMDB api with titles
        return self.metastore.find_metadata_by_titles(titles)


class TitleParser(object):

    """
        define methods such as abc_parser to register
        the method as an available parser function.
    """
    key = "parser"

    def __init__(self, title):
        self.title = title
        self.parsers = self._get_parsers()

    def _get_parsers(self):
        funcs = inspect.getmembers(self,
                                   predicate=inspect.ismethod)

        parsers = []
        for name, func in funcs:
            split = name.split('_')
            if len(split) > 1 and split[-1] == self.key:
                parsers.append(func)
        return parsers

    def parse(self):
        return map(lambda parser: parser(self.title).strip(), self.parsers)

    def dummy_parser(self, title):
        return title

    def clean_year_parser(self, title):
        exp = r'\(\d{4}\)'
        return re.sub(exp, '', title)

if __name__ == "__main__":
    title = 'Manhattan (1979)'
    parser = TitleParser(title)
    print parser.parse()