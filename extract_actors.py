"""
Given a path to a worker directory, 
gathers text and returns a set of possible actors
"""
from constants import MIN_L, MAX_L, MIN_NAME_L, MAX_NAME_L
from utils import flatten, write_log, ActorDB, valid_token_size, valid_name_size, parse_name
from pytesser import pytesser
from glob import glob

from fuzzywuzzy import process

import string
import itertools

EXT = ".png"

def get_actors(path, wildcard=EXT):
    """
        path: Input path where processed movie is contained
        Performs OCR on each image found at path/*wildcard.
        The text is then cleaned and normalized to the closest 
        match to known actors and actresses. 
        A set of names is returned.
    """

    cleaner = StringCleaner()
    img_paths = glob("%s/*%s" % (path, wildcard))

    img_text = map(_text_from_img, img_paths)
    write_log('img_text', img_text, path=path)

    clean_text = flatten(map(cleaner.clean, img_text))
    write_log('clean_text', clean_text, path=path)

    return clean_text

def _text_from_img(img_path):
    """
        return the text results of pytesser OCR
    """
    return pytesser.image_file_to_string(img_path)

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
        return set(filter(lambda x: valid_token_size(x) \
            and valid_name_size(x.split()), s))

if __name__ == "__main__":
    print get_actors('tmp/img')
