"""
    Process actor names from the OMDB database file
"""

from librarian.constants import PROGRESS
from librarian.utils import download_file, unzip_file
from librarian.identifiers.movies.credits.constants import ACTORS_CSV_HEADER
from librarian.identifiers.movies.credits.utils import parse_name
from populate_actors import OMDB_FILE_NAME

import csv
import os

REQ_URL = "http://www.beforethecode.net/projects/OMDb/download.aspx?e=joshblum@mit.edu"
OMDB_IN_FILE = "omdb.txt"
OMDB_OUT_FILE = "omdb_actors.csv"


def scrape_omdb(write_file, cleanup=True):
    """
        Download the omdb database file and process the data

    """
    local_file = download_file(REQ_URL)
    unzip_file(local_file)
    with open(OMDB_IN_FILE) as f_read, open(write_file, "w") as f_write:
        reader = csv.DictReader(f_read, delimiter="\t")
        writer = csv.DictWriter(f_write, ACTORS_CSV_HEADER)
        writer.writeheader()
        actor_count = 0
        for line in reader:
            clean_row = _clean_row(line)
            actor_count += len(clean_row)
            writer.writerows(clean_row)
            if not actor_count % PROGRESS:
                print "Found %d actors" % actor_count
    print "Found %d actors" % actor_count

    if cleanup:
        map(os.remove, [local_file, 'tomatoes.txt', OMDB_IN_FILE])


def _clean_row(line):
    """
        split a single row into a list of 
        dictionaries of first and last names for each actor
    """

    names = line['Cast'].split(",")
    name_pairs = map(parse_name, names)
    return [{
            'f_name': f_name,
            'l_name': l_name,
            } for f_name, l_name in name_pairs]

if __name__ == "__main__":
    scrape_omdb(OMDB_OUT_FILE, cleanup=True)
