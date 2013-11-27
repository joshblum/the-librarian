import os 

TMDB_API_KEY = "04a87a053afac639272eefbb94a173e4"
MAX_L = 30
MIN_L = 3
MIN_NAME_L = 2
PROGRESS = 1000
MAX_NAME_L = 4
ACTORS_CSV_HEADER = ["f_name", "l_name"]
SQL_CONFIG = {
	'csv_file' : 'actors.csv',
	'table_name' : 'actors',
	'cols' : ACTORS_CSV_HEADER,
	'len_diff' : 0,
}
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))