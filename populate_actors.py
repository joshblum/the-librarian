"""
    Scrape the most popular actors from the TMDB api and output to a file
"""

from tmdb import tmdb
from constants import TMDB_API_KEY, PROGRESS, MAX_L, MIN_L, ACTORS_CSV_HEADER
from utils import parse_name
import csv

tmdb.configure(TMDB_API_KEY)

OUTPUT_FILE = "actors.csv"


def populate_actors_file(write_file=OUTPUT_FILE, limit=False):
    tmp_name = "%s.tmp" % write_file
    scrape_actors(tmp_name, limit=limit)

    clean_scraped_data(tmp_name, write_file)

def scrape_actors(write_file, limit=False):
    """
        Call the tmdb api and write results of popular
        actors to the given file path
    """
    popular = tmdb.Popular(limit=limit)

    with open(write_file, "w") as f_write:
        writer = csv.DictWriter(f_write, ACTORS_CSV_HEADER)
        writer.writeheader()
        for i, res in enumerate(popular.iter_results()):
            if not isinstance(res, dict):
                continue
            writer.writerow(_clean_res(res))
            if not i % PROGRESS:
                print "Found %d actors" % i
    print "Found %d actors" % i

def _clean_res(res):
    clean_res = {}
    for k, v in res.iteritems():
        try:
            clean_res[k] = v.encode('ascii', 'ignore')
            if k == "name":
                del clean_res['name']
                first, last = parse_name(v)
                clean_res['f_name'] = first
                clean_res['l_name'] = last

        except:
            continue
    return clean_res

def clean_scraped_data(in_file, out_file):
    with open(in_file) as f_read, open(out_file, 'w') as f_write:
        reader = csv.DictReader(f_read)
        writer = csv.DictWriter(f_write, ACTORS_CSV_HEADER)
        writer.writeheader()
        dirty = 0
        for line in reader:
            if _clean_line(line):
                writer.writerow(line)
            else:
                dirty += 1
    print "Removed %d dirty lines." % dirty

def _clean_line(line):
    return _valid_name(line['f_name']) and _valid_name(line['l_name'])

def _valid_name(name):
    return len(name) > MIN_L and len(name) < MAX_L

if __name__ == "__main__":
    populate_actors_file(limit=True)
