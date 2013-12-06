"""
    Process actor names from the OMDB database file
"""

from librarian.constants import PROGRESS
from librarian.utils import download_file, unzip_file
from librarian.identifiers.movies.constants import ACTORS_CSV_HEADER, FILMS_CSV_HEADER
from librarian.identifiers.movies.utils import parse_name
from populate_actors import OMDB_FILE_NAME

import csv
import os

REQ_URL = "http://www.beforethecode.net/projects/OMDb/download.aspx?e=joshblum@mit.edu"
OMDB_IN_FILE = "omdb.txt"
OMDB_ACTORS_FILE = "omdb_actors.csv"
OMDB_FILMS_FILE = "films.csv"


def scrape_omdb(write_file, header,
                row_cleaner, data_type="", cleanup=True):
    """
        Download the omdb database file and process the data

    """
    write_file = os.path.join(os.path.dirname(__file__), write_file)
    local_file = download_file(REQ_URL)
    unzip_file(local_file)
    with open(OMDB_IN_FILE) as f_read, open(write_file, "w") as f_write:
        reader = csv.DictReader(f_read, delimiter="\t")
        writer = csv.DictWriter(f_write, header)
        writer.writeheader()
        count = 0
        for line in reader:
            clean_row = row_cleaner(line)
            count += len(clean_row)
            writer.writerows(clean_row)
            if not count % PROGRESS:
                print "Found %d %s" % (count, data_type)
    print "Found %d %s" % (count, data_type)

    if cleanup:
        map(os.remove, [local_file, 'tomatoes.txt', OMDB_IN_FILE])


def clean_actor_row(line):
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


def clean_film_row(line):
    """
        Return the film title and year
    """
    return [{
        'title': line['Title'].lower(),
        'year': line['Year'],
    }]

if __name__ == "__main__":
    scrape_omdb(OMDB_FILMS_FILE, FILMS_CSV_HEADER, 
        clean_film_row, "films", cleanup=False)
