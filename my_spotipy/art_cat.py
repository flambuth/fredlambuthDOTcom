from datetime import date
import sqlite3

from data_definition import make_insert_query, query_db
from data_definition import table_schemas, database

from daily_charts import Daily_Table

from fred_spotify import art_id_to_art_cat
from genres import inspect_tri_genres

today_date = date.today()
today_string = today_date.strftime('%Y-%m-%d')

def new_entry(
        art_id,
        corrected_entry=False,
        ):
    '''
    Returns a dictionary that has all the necessary fields to be an entry in the artist catalog
    Makes a Spotify API each time. 
    '''
    artist_data = art_id_to_art_cat(art_id)

    #takes the three genre tags from spotify, evalutes each for a 'master_genre'
    #then picks the most common one, or the first one if there is a tie.
    tri_genres = artist_data[3:6]
    artist_data.append(inspect_tri_genres(tri_genres))

    artist_data.append(today_string)

    #by default, new_entry means a first entry or a latest revision,
    #so the corrected_entry parameter defaults to False
    if corrected_entry==True:
        artist_data.append(False)
    else:
        artist_data.append(True)

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
        count_basie = '3mATHi0690pFOIG0VhalBL'
        art_ids_in_tracks = [i[0] for i in query_db("select distinct art_id from daily_tracks")]
        art_ids_in_arts = [i[0] for i in query_db("select distinct art_id from daily_artists")]
        all_possible_ids = list(set(art_ids_in_tracks + art_ids_in_arts))
        if count_basie in all_possible_ids:
            all_possible_ids.remove(count_basie)
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

    def add_records_to_catalog(
            self, 
            art_records):
        '''
        Accepts processed art_record dicts and inserts them into the artist_catalog table
        '''
        query = make_insert_query(self.table, self.col_names)
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        #executemany takes a lists of lists, not the usualy dictionary of lists
        cursor.executemany(query, art_records)
            
        sqliteConnection.commit()
        cursor.close()
        sqliteConnection.close()

    def scan_charts_and_insert(self):
        '''
        Job that looks through both daily charts to find if any art_ids there are not present
        in the artist catalog. If one or more is found, they are added to the catalog
        with the .add_to_catalog() method
        '''
        new_art_ids = self.ids_not_in_art_cat()
        if new_art_ids:
            self.add_to_catalog(new_art_ids)
        else:
            return 'No New Artists in Charts.'
        
    def refreshed_artist_catalog(self):
        '''
        Using all the art_ids in the current art_cat table as the iterable,
        the new_entry function calls the Spotify API to get new values for each
        art_id. 
        Uses todays date as the value for 'app_record_date'

        Takes about 3 minutes to make 970 API requests

        with open(csv_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(todays_art_cat)
        '''
        art_ids = self.art_ids
        todays_art_cat = list(map(new_entry, art_ids))
        return todays_art_cat
    
    def add_refreshed_records_to_art_cat(self):
        '''
        Encapsulates functions that:
            make SPotify API call for each art_id in art_cat
            process each API return into an art_cat record dict
            adds the art_cat record into the art_cat table
        '''
        new_a_c = self.refreshed_artist_catalog()
        self.add_records_to_catalog(new_a_c)
        return f'{today_string} is now the latest app_record_date for all entries'
        

if __name__ == '__main__':
    Artist_Catalog().scan_charts_and_insert()
#51kDu9CfyGBpcgMwy8MlEd
#4rC8J4M4aOqsQSCP4yoyJI