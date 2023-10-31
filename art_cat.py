from datetime import date
import sqlite3

from data_definition import make_insert_query, query_db
from data_definition import table_schemas, database

from daily_charts import Daily_Table

from fred_spotify import art_id_to_art_cat
from genres import inspect_tri_genres


def new_entry(art_id):
    '''
    Returns a dictionary that has all the necessary fields to be an entry in the artist catalog
    Makes a Spotify API each time. 
    '''
    artist_data = art_id_to_art_cat(art_id)

    today_date = date.today()
    today_string = today_date.strftime('%Y-%m-%d')

    tri_genres = artist_data[3:6]
    artist_data.append(inspect_tri_genres(tri_genres))

    artist_data.append(today_string)

    #my_spobj.first_appearance = self.find_first_appearance(art_id)

    return artist_data

class Artist_Catalog:
    def __init__(self, table='artist_catalog'):
        self.table = table
        self.col_names = [i[0] for i in  table_schemas[self.table]]

        self.art_cat = query_db('select * from artist_catalog;')
        self.art_ids = [i[0] for i in query_db('SELECT DISTINCT art_id FROM artist_catalog;')]
        self.artists = [i[0] for i in query_db('SELECT DISTINCT art_name FROM artist_catalog;')]


    def scan_latest_chart_for_new_artists(self):
        '''
        Checks ONLY the last daily chart for artists and tracks
        Returns a list of art_ids, or an empty list if there is nothing new
        '''
        latest_tracks = Daily_Table('daily_tracks').latest_art_ids
        latest_arts = Daily_Table('daily_artists').latest_art_ids
        latest_art_ids = list(set(latest_tracks + latest_arts))
        new_ids = [i for i in latest_art_ids if i not in self.art_ids]

        return new_ids

    def ids_not_in_art_cat(self):
        '''
        Checks ALL of the daily chart history for both chart types
        '''
        art_ids_in_tracks = [i[0] for i in query_db("select distinct art_id from daily_tracks")]
        art_ids_in_arts = [i[0] for i in query_db("select distinct art_id from daily_artists")]
        all_possible_ids = list(set(art_ids_in_tracks + art_ids_in_arts))
        return [i for i in all_possible_ids if i not in self.art_ids]


    def add_to_catalog(
            self, 
            art_ids):
        '''
        Accepts art_ids and insert an art_car record of them into the artist_catalog table
        '''
        new_art_cat_records = list(map(new_entry, art_ids))

        query = make_insert_query(self.table, self.col_names)
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        #executemany takes a lists of lists, not the usualy dictionary of lists
        cursor.executemany(query, new_art_cat_records)
            
        sqliteConnection.commit()
        cursor.close()
        sqliteConnection.close()

    def scan_charts_and_insert(self):
        new_art_ids = self.ids_not_in_art_cat()
        if new_art_ids:
            self.add_to_catalog(new_art_ids)
        else:
            return 'No New Artists in Charts.'
        

if __name__ == '__main__':
    Artist_Catalog().scan_charts_and_insert()
#51kDu9CfyGBpcgMwy8MlEd
#4rC8J4M4aOqsQSCP4yoyJI