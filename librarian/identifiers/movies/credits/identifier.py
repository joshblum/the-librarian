"""
    Movie credit identification handler.
    Create this object with an input file
"""

from librarian.constants import LOGGING
from librarian.identifiers.identifiers import MovieIdentifier
from extract_frames import extract_frames
from extract_credits import extract_credits
from find_films import find_films

import pipes
import os
import logging.config

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class MovieCreditIdentifier(MovieIdentifier):

    def __init__(self, srcfile, path):
        super(MovieIdentifier, self).__init__(srcfile, path)
        self.srcfile = pipes.quote(self.srcfile)
        self.credits_path = "%s/credits" % self.path
        if not os.path.exists(self.credits_path):
            os.mkdir(self.credits_path)

    def get_titles(self):
        #optimization: stream frames instead of batch
        extract_frames(self.srcfile, self.path, self.credits_path)
        logger.debug("Retrieving credit tokens.")

        credit_tokens = extract_credits(self.credits_path)

        films = find_films(credit_tokens)
        logger.debug(films)
        return films

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        ident = MovieCreditIdentifier(sys.argv[1], "/tmp")
        print ident.identify()
