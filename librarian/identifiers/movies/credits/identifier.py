"""
    Movie credit identification handler.
    Create this object with an input file
"""

from librarian.constants import LOGGING
from librarian.identifiers.identifier_base import MovieIdentifier
from extract_frames import extract_frames
from extract_credits import extract_credits
from find_films import find_films

import os
import logging.config

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class MovieCreditIdentifier(MovieIdentifier):

    def __init__(self, srcfile, cleanup=True):
        super(MovieIdentifier, self).__init__(srcfile, cleanup)
        self.credits_path = "%s/credits" % self.path
        os.mkdir(self.credits_path)

    def get_titles(self):

        extract_frames(self.srcfile, self.path, self.credits_path)
        logger.debug("Retrieving credit tokens.")

        credit_tokens = extract_credits(self.credits_path)
        logger.debug(credit_tokens)

        films = find_films(credit_tokens)
        logger.debug(films)
        return films


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        ident = MovieCreditIdentifier(sys.argv[1])
        print ident.identify()
