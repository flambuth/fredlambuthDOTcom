import sqlite3

from data_definition import make_insert_query, query_db
from data_definition import table_schemas, database

from fred_spotify import song_id_to_track_cat
#from daily_charts import Daily_Table


def ids_not_in_track_cat():
    '''
    Checks ALL of the daily chart history for both chart types
    Returns a list of song_ids
    '''
    song_ids_in_tracks = [i[0] for i in query_db("select distinct song_id from daily_tracks")]
    song_ids_in_track_cat = [i[0] for i in query_db("select distinct song_id from track_catalog")]

    tracks_not_in_track_cat = [
        i for i in song_ids_in_tracks if i not in song_ids_in_track_cat
    ]

    return tracks_not_in_track_cat

def track_entries_not_in_track_cat(song_ids):
    '''
    Converts the track_ids that are not in track_cat into track_cat entries
    '''
    missing_track_cats = list(map(
    song_id_to_track_cat, song_ids
    ))
    return missing_track_cats

def add_track_to_catalog(track_entries):
    '''
    Accepts track_entries objects ready to be inserted into database
    Inserts them into the track_catalog table in the database
    '''
    table = 'track_catalog'
    col_names = table_schemas[table]

    query = make_insert_query(table, col_names)
    sqliteConnection = sqlite3.connect(database)
    cursor = sqliteConnection.cursor()
    #executemany takes a lists of lists, not the usualy dictionary of lists
    cursor.executemany(query, track_entries)
        
    sqliteConnection.commit()
    cursor.close()
    sqliteConnection.close()