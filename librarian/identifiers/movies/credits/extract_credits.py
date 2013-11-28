"""
    Given a path to a worker directory, 
    gathers text and returns a set of possible actors
"""

from utils import parse_name
from librarian.constants import LOGGING
from librarian.utils import flatten
from fuzzywuzzy import process
from pytesser import pytesser
from glob import glob

from utils import valid_token_size, valid_name_size
from constants import MIN_L, MAX_L, MIN_NAME_L, MAX_NAME_L

import string
import itertools
import logging.config

EXT = ".png"

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


def extract_credits(path, wildcard=EXT):
    """
        path: Input path where processed movie is contained
        Performs OCR on each image found at path/*wildcard.
        The text is then cleaned and normalized to the closest 
        match to known actors and actresses. 
        A set of names is returned.
    """
    logger.debug("Extracting credits at %s" % path)

    cleaner = StringCleaner()

    img_paths = glob("%s/*%s" % (path, wildcard))
    img_text = [_text_from_img(img_path, path) for img_path in img_paths]
    logger.debug("img_text %s" % img_text)

    clean_text = flatten(map(cleaner.clean, img_text))
    logger.debug("clean_text %s" % clean_text)

    return clean_text


def _text_from_img(img_path, path):
    """
        return the text results of pytesser OCR
    """
    # potential optimization:
    # only OCR that are x% black
    return pytesser.image_file_to_string(img_path, path=path)


def _split_text(clean_text):
    """
        split text into terms for fuzzy matching
    """
    return flatten(map(
        lambda tokens: map(parse_name, tokens), clean_text))


def _map_args(func, arg1, arg2):
    """
        wrapper for mapping two args to a function
        should be made more general
    """
    return map(func, arg1, itertools.repeat(arg2, len(arg1)))


class StringCleaner(object):

    def __init__(self, min_l=MIN_L, max_l=MAX_L):
        self.min_l = min_l
        self.max_l = max_l
        self.table = string.maketrans("", "")
        self.exclude_chars = "%s%s" % (string.punctuation, string.digits)

    def clean(self, s):
        """
            Reduce the search space by filtering by string size
            and clearing whitespace
        """
        return self._filter_tokens(
            self._strip_tokens(
                self._asciify(
                    self._rm_punc(
                        self._tokenize(s)
                    )
                )
            )
        )

    def _tokenize(self, s):
        return s.lower().split("\n")

    def _rm_punc(self, s_list):
        return map(lambda s:
                   s.translate(self.table, self.exclude_chars), s_list)

    def _asciify(self, s_list):
        clean = []
        for s in s_list:
            try:
                clean.append(s.encode('ascii', 'ignore'))
            except Exception:
                continue
        return clean

    def _strip_tokens(self, s_list):
        return map(lambda s: s.strip(), s_list)

    def _filter_tokens(self, s):
        return set(filter(lambda x: valid_token_size(x)
                          and valid_name_size(x.split()), s))

if __name__ == "__main__":
    print extract_credits('tmp/img')
