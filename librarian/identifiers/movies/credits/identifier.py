"""
    Movie credit identification handler.
    Create this object with an input file
"""

from librarian.identifiers.identifier_base import MovieIdentifier
from extract_frames import extract_frames
from extract_credits import extract_credits
from find_films import find_films

import os


class MovieCreditIdentifier(MovieIdentifier):

    def __init__(self, srcfile):
        super(MovieIdentifier, self).__init__(srcfile)
        self.credits_path = "%s/credits" % self.path
        os.mkdir(self.credits_path)

    def find_titles(self):
        extract_frames(self.srcfile, self.path, self.credits_path)
        credit_tokens = extract_credits(self.credits_path)
        return find_films(credit_tokens)


if __name__ == "__main__":
    ident = MovieCreditIdentifier('/Users/joshblum/Dropbox/code/the-librarian/tmp/test.mp4')
    print ident.identify()
