from librarian.constants import PROGRESS
from librarian.utils import flatten
from librarian.identifiers.movies.constants import ACTORS_CSV_HEADER
from librarian.identifiers.movies.utils import parse_name, valid_token_size
import csv

TMDB_FILE_NAME = "tmdb_actors.csv"
OMDB_FILE_NAME = "omdb_actors.csv"
OUTPUT_FILE = "actors.csv"
INPUT_FILES = [TMDB_FILE_NAME, OMDB_FILE_NAME]


def populate_actors_file(input_files=INPUT_FILES,
                         write_file=OUTPUT_FILE, cleanup=True):

    data = set(
        map(tuple,
            flatten(
                map(clean_scraped_data, input_files)
            )
            )
    )
    data_dicts = map(lambda x: {
        'f_name': x[0],
        'l_name': x[1],
    }, data)
    write_scraped_data(write_file, data_dicts)

    if cleanup:
        map(os.remove, INPUT_FILES)


def clean_scraped_data(in_file):
    with open(in_file) as f_read:
        reader = csv.DictReader(f_read)
        data = []
        dirty = 0
        for i, line in enumerate(reader):
            if _is_clean_line(line):
                line = _process_line(line)
                data.append(line)
            else:
                dirty += 1

            if not i % PROGRESS:
                print "Processed %d lines" % i

    print "Removed %d dirty lines." % dirty
    return data


def write_scraped_data(write_file, data):
    with open(write_file, 'w') as f_write:
        writer = csv.DictWriter(f_write, ACTORS_CSV_HEADER)
        writer.writeheader()
        writer.writerows(data)


def _is_clean_line(line):
    return valid_token_size(line['f_name']) and valid_token_size(line['l_name'])


def _process_line(line):
    line = [line[k].lower() for k in ACTORS_CSV_HEADER]
    for i in range(len(line)):
        try:
            val = line[i].encode('ascii', 'ignore')
        except:
            val = ""
        line[i] = val
    return line


if __name__ == "__main__":
    populate_actors_file(cleanup=True)
