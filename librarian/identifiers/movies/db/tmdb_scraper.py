"""
    Scrape the most popular actors from the TMDB api and output to a file
"""
from tmdb import tmdb
from librarian.identifiers.movies.utils import parse_name
from librarian.constants import TMDB_API_KEY, PROGRESS
from populate_actors import TMDB_FILE_NAME

import csv

tmdb.configure(TMDB_API_KEY)

TMDB_CSV_HEADER = ["adult", "id", "f_name",
                   "l_name", "popularity", "profile_path", ]


def scrape_tmdb(write_file, limit=False):
    """
        Call the tmdb api and write results of popular
        actors to the given file path
    """
    popular = tmdb.Popular(limit=limit)

    with open(write_file, "w") as f_write:
        writer = csv.DictWriter(f_write, TMDB_CSV_HEADER)
        writer.writeheader()
        for i, res in enumerate(popular.iter_results()):
            if not isinstance(res, dict):
                continue
            writer.writerow(_clean_res(res))
            if not i % PROGRESS:
                print "Found %d actors" % i
    print "Found %d actors" % i


def _clean_res(res):
    clean_res = {
        'f_name': "",
        'l_name': "",
    }
    for k, v in res.iteritems():
        if k == "name":
            try:
                v = v.encode('ascii', 'ignore')
                first, last = parse_name(v)
                clean_res['f_name'] = first
                clean_res['l_name'] = last

            except Exception, e:
                pass
        else:
            clean_res[k] = v

    return clean_res

if __name__ == "__main__":

    scrape_tmdb(TMDB_FILE_NAME, limit=True)
