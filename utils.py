"""
    utils module containing common helper functions
"""

from datetime import datetime, timedelta
from constants import SQL_CONFIG, MIN_L, MAX_L, MIN_NAME_L, MAX_NAME_L
import requests
import cPickle
import shutil
import uuid
import os
import csv
import sqlite3
import zipfile

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
MIN = 5
FMT = "%H:%M:%S"


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
        print "Writing %s" % file_name
    with open("%s/%s" % (path, file_name), 'w') as f:
        f.write(str(data))


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
    return _between_values(split_name, MIN_NAME_L, MAX_NAME_L, inclusive=True)


def valid_token_size(token):
    return _between_values(token, MIN_L, MAX_L)


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


def download_file(url):
    local_filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
    return local_filename


def unzip_file(filename, dest_dir="."):
    with zipfile.ZipFile(filename) as zf:
        for member in zf.infolist():
            # Path traversal defense copied from
            # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
            words = member.filename.split('/')
            path = dest_dir
            for word in words[:-1]:
                drive, word = os.path.splitdrive(word)
                head, word = os.path.split(word)
                if word in (os.curdir, os.pardir, ''):
                    continue
                path = os.path.join(path, word)
            zf.extract(member, path)


def get_time_delta(date):
    date = date.split(".")[0]
    date = datetime.strptime(date, FMT)
    delta = timedelta(minutes=MIN)
    return (date - delta).strftime(FMT)
