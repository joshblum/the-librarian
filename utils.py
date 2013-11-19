"""
    utils module containing common helper functions
"""
from constants import SQL_CONFIG, MIN_NAME_L, MAX_NAME_L

import cPickle
import shutil
import uuid
import os
import csv
import sqlite3

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))


def _create_path():
    """
        create a directory and return the absolute path
    """
    dirname = str(uuid.uuid4())
    path = os.path.join(ROOT_PATH, dirname)
    os.mkdir(path)
    return path


def tmp_dir_wrap(func):
    """
        decorator to wrap video get functions.
        creates and then removes a tmp dir 
        return results of wrapped function
    """
    def init_wrapper(*args, **kwargs):
        path = _create_path()
        res = None

        try:
            res = func(path, *args, **kwargs)

        except Exception, e:
            print e

        finally:
            shutil.rmtree(path)

        return res

    return init_wrapper


def flatten(l):
    return [item for sublist in l for item in sublist]


def write_log(file_name, data, path=""):
    try:
        print "Writing %s, %d lines long" % (file_name, len(data))
    except:
        pass
    with open("%s/%s" % (path, file_name), 'w') as f:
        f.write(str(data))

def parse_name(name):
    """
        returns a tuple of first name last name
        if it exists or None
    """
    name = name.split()
    if not valid_name_size(name):
        return "", ""
    return name[0], " ".join(name[1:])

def valid_name_size(split_name):
    return _between_values(split_name, MIN_NAME_L, MAX_NAME_L, inclusive=True)

def valid_token_size(token):
    return _between_values(split_name, MIN_NAME_L, MAX_NAME_L)

def _between_values(size, min_size, max_size, inclusive=False):
    assert min_size <= max_size
    try:
        size = len(size)
    except TypeError: 
        pass
    if inclusive:
        return size >= min_size and size <= max_size
    return size > min_size and size < max_size

def csv_to_sql(in_file, table_name, cols):
    cols_str = ", ".join(cols)
    vals = ", ".join(["?"] * len(cols))

    create_table_statement = "CREATE TABLE %s (%s);" % (table_name, cols_str)
    insert_statement = "INSERT INTO %s (%s) VALUES (%s);" % (
        table_name, cols_str, vals)

    with open(in_file) as f_read:
        con = sqlite3.connect(":memory:")
        cur = con.cursor()
        cur.execute(create_table_statement)

        reader = csv.DictReader(f_read)
        db = [[line[col] for col in cols] for line in reader]
        cur.executemany(insert_statement, db)
        con.commit()
        return con


class ActorDB(object):

    def __init__(self, config=SQL_CONFIG):
        self.config = config
        self.con = csv_to_sql(
            config['csv_file'], config['table_name'], config['cols'])
        self.cursor = self.con.cursor()

    def _fetchall(self, query):
        return flatten(self.cursor.execute(query).fetchall())

    def query_name(self, f_name, l_name):
        """
            find the intersection of all first and 
            last names are within len_diff size of the given name
        """
        values = {
            'f_name': f_name,
            'l_name': l_name,
        }
        values.update(self.config)
        query = """SELECT f_name, l_name FROM %(table_name)s 
                WHERE ABS(LENGTH(f_name) - LENGTH('%(f_name)s')) <= %(len_diff)s
                AND
                WHERE ABS(LENGTH(l_name) - LENGTH('%(l_name)s')) <= %(len_diff)s""" % values
        return self._fetchall(query)

    def get_name_id_pairs(self, names):
        values = {
            'names': names,
        }
        values.update(self.config)
        query =  """SELECT name, id FROM %(table_name)s 
                WHERE name in %(names)s""" % values
        return self.cursor.execute(query).fetchall()
