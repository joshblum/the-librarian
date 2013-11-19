TMDB_API_KEY = "04a87a053afac639272eefbb94a173e4"
PROGRESS = 1000
MAX_L = 30
MIN_L = 3
MIN_NAME_L = 2
MAX_NAME_L = 4

ACTORS_CSV_HEADER = ["adult", "id", "f_name", "l_name", "popularity", "profile_path", ]
SQL_CONFIG = {
	'csv_file' : 'actors.csv',
	'table_name' : 'actors',
	'cols' : ACTORS_CSV_HEADER,
	'len_diff' : 1,
}