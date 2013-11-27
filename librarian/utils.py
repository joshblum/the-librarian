"""
    utils module containing common helper functions
"""

from datetime import datetime, timedelta
from constants import ROOT_PATH

import requests
import os
import csv
import sqlite3
import zipfile

MIN = 5
FMT = "%H:%M:%S"


def flatten(l):
    return [item for sublist in l for item in sublist]


def write_log(file_name, data, path=""):
    try:
        print "Writing %s, %d lines long" % (file_name, len(data))
    except:
        print "Writing %s" % file_name
    with open("%s/%s" % (path, file_name), 'w') as f:
        f.write(str(data))

def between_values(size, min_size, max_size, inclusive=False):
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
