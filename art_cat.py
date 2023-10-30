from datetime import date
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
        self.art_cat = query_db('select * from artist_catalog;')
        self.art_ids = [i[0] for i in query_db('SELECT DISTINCT art_id FROM artist_catalog;')]
        self.artists = [i[0] for i in query_db('SELECT DISTINCT art_name FROM artist_catalog;')]


    def scan_latest_chart_for_new_artists(self):
        latest_tracks = Daily_Table('daily_tracks').latest_art_ids
        latest_arts = Daily_Table('daily_artists').latest_art_ids

        latest_art_ids = list(set(latest_tracks + latest_arts))

        new_ids = [i for i in latest_art_ids if i not in self.art_ids]

        return new_ids

#51kDu9CfyGBpcgMwy8MlEd
#4rC8J4M4aOqsQSCP4yoyJI