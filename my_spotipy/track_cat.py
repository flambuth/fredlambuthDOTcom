import sqlite3

from data_definition import make_insert_query, query_db
from data_definition import table_schemas, database

from fred_spotify import song_id_to_track_cat
#from daily_charts import Daily_Table

class Track_Catalog:
    def __init__(self, table='track_catalog'):
        self.table = table
        self.col_names = [i[0] for i in  table_schemas[self.table]]

        self.art_cat = query_db('select * from track_catalog;')
        self.track_ids = [i[0] for i in query_db('SELECT DISTINCT song_id FROM track_catalog;')]
        self.songs = [i[0] for i in query_db('SELECT DISTINCT song_name FROM track_catalog;')]

    def add_track_to_catalog(
            self,
            track_entries
            ):
        '''
        Accepts track_entries objects ready to be inserted into database
        Inserts them into the track_catalog table in the database
        '''

        query = make_insert_query(self.table, self.col_names)
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        #executemany takes a lists of lists, not the usualy dictionary of lists
        cursor.executemany(query, track_entries)
            
        sqliteConnection.commit()
        cursor.close()
        sqliteConnection.close()

    def scan_charts_and_insert(self):
        '''
        Job that looks through both daily charts to find if any art_ids there are not present
        in the artist catalog. If one or more is found, they are added to the catalog
        with the .add_to_catalog() method
        '''
        new_song_ids = self.ids_not_in_track_cat()
        if new_song_ids:
            self.add_track_to_catalog(new_song_ids)
        else:
            return 'No New Artists in Charts.'

    @classmethod
    def ids_not_in_track_cat(cls):
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

    @staticmethod
    def track_entries_from_song_ids(song_ids):
        '''
        Maps the fred_spotify.song_id_to_track_cat function to a list of art_ids
        '''
        missing_track_cats = list(map(
            song_id_to_track_cat, song_ids
        ))
        list_of_lists = [list(d.values()) for d in missing_track_cats]
        return list_of_lists

if __name__ == '__main__':
    Track_Catalog().scan_charts_and_insert()