"""
    Movie title identification handler.
    Create this object with a srcfile that contains the title
"""

from librarian.constants import LOGGING, VIDEO_EXT
from librarian.utils import flatten
from librarian.identifiers.identifiers import MovieIdentifier

from librarian.identifiers.movies.utils import FilmDB

import logging.config
import inspect
import os
import re

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

YEAR = r'\d{4}'

STOPWORDS = set([
    'avi', '', 'dvdrip', 'xvid', 'axxo', 'eng', 'nfo', 'txt', 'donatello', 'axial', 'mi2', 'alli', 'p2p', 'sample', 'srt', 'jpg', 'subs', 'ac3', 'com', 'cd1', 'demonoid', 'fxg', 'thereaderb', 'cd2', 'thereadera', 'klaxxon', 'in', 'sub', 'edition', 'mkv', 'rar', 'trailer', 'dmd',
    'divx', 'dvd', 'unrated', 'png', 'sfv', 'theatrical', 'vob', 'dvdscr', 'dr', 'ii', 'x264', 'www', 'cover', 'documentary', 'limited', 'downloaded', 'read', 'part', 'torrent', 'mbc', 'cdcovers_cc', 'frontcover', '720p', 'iii', 'special', 'ws',  'waf', 'dts',  'rip', 'ue', 'bluray']).union(VIDEO_EXT)

def check_stop_words(token):
    replace = ["(", ")", "[", "]"]
    for r in replace:
        token.replace(r, "")
    return token not in STOPWORDS

class MovieTitleIdentifier(MovieIdentifier):

    def __init__(self, srcfile, path):
        super(MovieTitleIdentifier, self).__init__(srcfile, path)
        self.db = FilmDB()
        self.title = os.path.basename(srcfile)
        self.parser = TitleParser(self.title)

    def get_titles(self):
        possible_titles = self.parser.parse()
        logger.debug("Found possible titles %s for title %s" % (possible_titles, self.title))
        possible_exact_titles = flatten(
            [self.db.query_title(title, year) for title, year in possible_titles])
        possible_fuzzy_titles = flatten(
            [self.db.query_fuzzy(title, year) for title, year in possible_titles])
        
        titles = set(possible_exact_titles).intersection(set(possible_fuzzy_titles))
        logger.debug("Found normalized titles %s" % titles)
        return titles

    def get_params(self, title):
        title, year = title
        params = {
            't': title,
            'tomatoes': True,
        }
        if year:
            params['y'] = year
        return params


class TitleParser(object):

    """
        define methods such as abc_parser to register
        the method as an available parser function.
    """
    key = "parser"

    def __init__(self, title):
        self.title = self.clean_title(title)
        self.years = re.findall(YEAR, title)

    def clean_title(self, title):
        """
            Remove all stop words.
        """
        title = re.sub(YEAR, "", title).lower()
        title = re.findall(r"[\w'\(\)\[\]]+", title)
        title = filter(check_stop_words, title)
        if len(title) and title[-1] == 'the':
            title = [title[-1]] + title[:-1]
        return " ".join(title).replace('"', "'")

    def parse(self):
        if not len(self.years):
            self.years = ['']
        return [(self.title, year) for year in self.years]


if __name__ == "__main__":
    titles = [
        'Spiderman 1 sample.avi', '(500) days of summer','Spiderman 2 sample.avi', 'Spider_Man-front.jpg', 'Go.avi', "Rosemary's Baby.avi", 'hackers2.jpg', 'Hackers (1995)', 'Hackers 2 (2000) - Operation TakeDown', '1.jpg', 'hackers1.jpg', 'info.txt', 'Thumbs.db', 'SubTitles', 'covers', 'Hackers.avi', 'EN', 'GR', '!!', 'Hackers.srt', 'Other GR Subs.rar', 'GR', 'Hackers.sub', 'Hackers.srt', 'Hackers-[cdcovers_cc]-front.jpg', 'Hackers_Canadian-[cdcovers_cc]-front.jpg', 'Hackers-[cdcovers_cc]-inside.jpg', 'Hackers_Widescreen-[cdcovers_cc]-front.jpg', 'Hackers_1_And_2-[cdcovers_cc]-front.jpg',
        'Hackers_R4-[cdcovers_cc]-inside.jpg', 'poster1.jpg', 'Hackers_R4-[cdcovers_cc]-front.jpg', 'Hackers_Widescreen-[cdcovers_cc]-cd1.jpg', 'Hackers-[cdcovers_cc]-cd1.jpg', 'Hackers_R4-[cdcovers_cc]-inlay.jpg', 'Hackers_R4-[cdcovers_cc]-cd1.jpg', 'SubTitles', 'Hackers 2 - Operation Takedown.avi', 'Covers', 'GR', 'SP', 'Hackers 2 - Operation Takedown.srt', 'Hackers 2 - Operation Takedown.srt', 'Hackers_2_Takedown_French-[cdcovers_cc]-cd1.jpg', 'Hackers_2_Takedown_custom-[cdcovers_cc]-front.jpg', 'Hackers_2_Takedown-[cdcovers_cc]-cd1.jpg', 'Hackers_1_And_2-[cdcovers_cc]-front.jpg', ]
    for title in titles:
        ident = MovieTitleIdentifier(title, "")
        parser = TitleParser(title)
        logger.debug("%s, %s" % (parser.parse(), ident.get_titles()))
