from librarian.utils import csv_to_sql, between_values

from librarian.identifiers.movies.constants import MIN_L, \
    MAX_L, MAX_NAME_L, MIN_NAME_L, ACTORS_SQL_CONFIG, FILMS_SQL_CONFIG

from fuzzywuzzy import process

import re

MIN_FUZZ_SCORE = 85

class DBWrap(object):

    def __init__(self, config):
        self.config = config
        self.con = csv_to_sql(
            config['csv_file'], config['table_name'], config['cols'])
        self.cursor = self.con.cursor()

    def fuzzy_match(self, token):
        """
            Perform fuzzing matching to try and match name tokens
        """
        choices = self.query_fuzzy(token)
        matches = process.extractOne(token, choices)
        if not isinstance(matches, list):
            matches = [matches]

        filtered_matches = filter(
            lambda x: x is not None and x[1] > MIN_FUZZ_SCORE, matches)
        return map(lambda x: x[0], filtered_matches)

    def query_fuzzy(self, token):
        raise NotImplementedError

    def _get_values(self, **kwargs):
        kwargs.update(self.config)
        return kwargs

    def _fetchall(self, query):
        return self.cursor.execute(query).fetchall()

    def _process_query(self, query):
        return self._fetchall(query)


class ActorDB(DBWrap):

    def __init__(self, config=ACTORS_SQL_CONFIG):
        super(FilmDB, self).__init__(config)

    def _get_name_token_values(self, name_token):
        f_name, l_name = parse_name(name_token)
        return self._get_values(f_name=f_name, l_name=l_name)

    def query_fuzzy(self, name_token):
        """
            find the intersection of all first and 
            last names are within len_diff size of the given name
        """
        values = self._get_name_token_values(name_token)
        query = """SELECT f_name, l_name FROM %(table_name)s 
                WHERE ABS(LENGTH(f_name) - LENGTH('%(f_name)s')) <= %(len_diff)s
                AND ABS(LENGTH(l_name) - LENGTH('%(l_name)s')) <= %(len_diff)s""" % values
        return self._process_query(query)

    def query_name(self, name_token):
        values = self._get_name_token_values(name_token)
        query = """SELECT f_name, l_name FROM %(table_name)s 
                WHERE f_name='%(f_name)s' AND l_name='%(l_name)s'""" % values
        return self._process_query(query)

    def _process_query(self, query):
        return map(lambda x: " ".join(x), self._fetchall(query))


class FilmDB(DBWrap):

    def __init__(self, config=FILMS_SQL_CONFIG):
        super(FilmDB, self).__init__(config)

    def query_title(self, title, year=""):
        values = self._get_values(title=title, year=year)
        query = """SELECT title, year from %(table_name)s
                WHERE title="%(title)s" """
        if year:
            query += " AND year='%(year)s'"
        return self._process_query(query % values)

    def query_fuzzy(self, title, year=""):
        values = self._get_values(title=title, year=year)
        query = """SELECT title, year FROM %(table_name)s 
                WHERE ABS(LENGTH(title) - LENGTH("%(title)s")) <= %(len_diff)s""" % values
        if year:
            query += " AND year='%(year)s'"
        return self._process_query(query % values)


def parse_name(name):
    """
        returns a tuple of first name last name
        if it exists or None
    """
    name = name.lower().split()
    if not valid_name_size(name):
        return "", ""
    return name[0], " ".join(name[1:])


def valid_name_size(split_name):
    return between_values(split_name, MIN_NAME_L, MAX_NAME_L, inclusive=True)


def valid_token_size(token):
    return between_values(token, MIN_L, MAX_L)
