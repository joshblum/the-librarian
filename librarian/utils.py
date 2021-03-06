"""
    utils module containing common helper functions
"""

from datetime import datetime, timedelta
from constants import ROOT_PATH

import hashlib
import requests
import os
import csv
import sqlite3
import zipfile

MIN = 5
FMT = "%H:%M:%S"


def flatten(l):
    return [item for sublist in l for item in sublist]


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
        con.text_factory = str
        cur = con.cursor()
        cur.execute(create_table_statement)

        reader = csv.DictReader(f_read)
        db = [[line[col] for col in cols] for line in reader]
        cur.executemany(insert_statement, db)
        con.commit()
        return con


def download_file(url):
    local_filename = url.split('/')[-1]
    local_filename = os.path.join(
        os.path.dirname(__file__), local_filename)
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


def md5_for_file(path, block_size=256 * 128, hr=False):
    """
    Block size directly depends on the block size of your filesystem
    to avoid performances issues
    Here I have blocks of 4096 octets (Default NTFS)
    """
    md5 = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(block_size), b''):
            md5.update(chunk)
    if hr:
        return md5.hexdigest()
    return md5.digest()
