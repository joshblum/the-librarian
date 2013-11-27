from librarian.utils import csv_to_sql, between_values

from constants import MIN_L, MAX_L, MAX_NAME_L, MIN_NAME_L, SQL_CONFIG


class ActorDB(object):

    def __init__(self, config=SQL_CONFIG):
        self.config = config
        self.con = csv_to_sql(
            config['csv_file'], config['table_name'], config['cols'])
        self.cursor = self.con.cursor()

    def _fetchall(self, query):
        return self.cursor.execute(query).fetchall()

    def _process_query(self, query):
        return map(lambda x: " ".join(x), self._fetchall(query))

    def _get_name_token_values(self, name_token):
        f_name, l_name = parse_name(name_token)
        values = {
            'f_name': f_name,
            'l_name': l_name,
        }
        values.update(self.config)
        return values

    def query_close_name(self, name_token):
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
