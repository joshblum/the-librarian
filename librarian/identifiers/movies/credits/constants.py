MAX_L = 30
MIN_L = 3
MIN_NAME_L = 2
MAX_NAME_L = 4
ACTORS_CSV_HEADER = ["f_name", "l_name"]

import os 
SQL_CONFIG = {
    'csv_file' : os.path.join(os.path.dirname(__file__), 'db/actors.csv'),
    'table_name' : 'actors',
    'cols' : ACTORS_CSV_HEADER,
    'len_diff' : 0,
}