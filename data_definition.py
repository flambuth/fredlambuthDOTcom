import sqlite3
import json
from genres import inspect_tri_genres
#from daily_charts import make_insert_query

database = 'fredlambuth.db'
tables = [
    #appended once per day
    'daily_tracks',
    'daily_artists',
    #appended every few minutes if Spotify played a new song
    'recently_played',
    #dimension tables of artists and songs found in daily_tracks and daily_artists
    'artist_catalog',
    'track_catalog']
table_schemas = {
        'artist_catalog' : [
            ('art_id', 'TEXT'),
            ('art_name', 'TEXT'),
            ('followers', 'INTEGER'),
            ('genre1', 'TEXT NULL'),
            ('genre2', 'TEXT NULL'),
            ('genre3', 'TEXT NULL'),
            ('img_url', 'TEXT NULL'),
            ('img_url_mid', 'TEXT NULL'),
            ('img_url_sml', 'TEXT NULL'),
            ('master_genre', 'TEXT NULL'),
            ('app_record_date', 'datetime'),],

        'track_catalog' : [
            ('art_name', 'TEXT'),
            ('album_id', 'TEXT'),
            ('album_name', 'TEXT'),
            ('song_id', 'TEXT'),
            ('song_name', 'TEXT'),
            ('img_url', 'TEXT NULL'),
            ('duration', 'INTEGER'),
            ('app_record_date', 'datetime'),
            ],

        'daily_tracks' :[('position', 'INTEGER'),
            ('art_id', 'TEXT'),
            ('art_name', 'TEXT'),
            ('album_name', 'TEXT NULL'),
            ('song_id', 'TEXT'),
            ('song_name', 'TEXT'),
            ('date', 'datetime'),],
        'daily_artists':[('position', 'INTEGER'),
            ('art_id', 'TEXT'),
            ('art_name', 'TEXT'),
            ('date', 'datetime'),],

        'recently_played':[('art_name', 'TEXT'),
            ('song_name', 'TEXT'),
            ('song_link', 'TEXT'),
            ('image', 'TEXT'),
            ('last_played', 'TEXT'),]}

#functions to make the SQLITE queries that do the CRUD operations
def make_question_marks(cols):
    '''
    Returns the string with the right amount of ?s and commas in between them for a SQL INSERT statement
    '''
    n = len(cols)
    marks = '?,'*n
    marks = marks[:-1]
    return marks

def make_insert_query(table, col_names):
    '''
    Creates a SQLite3 friendly insert statement that can fit on any of the 4 tables stashed as an object variable.
    '''
    marks = make_question_marks(col_names)
    col_string = ','.join(col_names)
    insert_sql = f'''INSERT INTO {table} ({col_string}) VALUES ({marks}) '''
    return insert_sql

def query_db(query):
    '''
    Returns a set of .fetchall() restults from the db

    YOU NEED TO MIGRATE BEFORE THIS CAN WORK! (july 16,2022)
    '''
    try:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return results
        #cursor.close()
    except sqlite3.Error as error:
        print("This error happens because your shortcut for querying SQLITE did not work", error)
    finally:
        if (conn):
            conn.close()



class Data_Definition:
    def __init__(self):
        self.woah = 'this whole time I should have been using class variables'

    def make_create_query(self, table_name):
        '''
        Assembles a CREATE TABLE SQL statement.
        Assigns an 'id' column as the primary field.
        Also includes a DROP TABLE statement if the table exists.

        '''
        header = f'DROP TABLE IF EXISTS {table_name};\n'
        header += f'CREATE TABLE {table_name} ( id INTEGER PRIMARY KEY,'
        footer = ');'
        col_tuples = table_schemas[table_name]
        # makes a list of rows for each entry from the table_schemas tuples
        list_of_rows = [f'{i[0]} {i[1]},' for i in col_tuples]
        # drops the last comma. Apparently that really matters to sqlite3
        list_of_rows[-1] = list_of_rows[-1][:-1]
        fields = ' '.join(list_of_rows)

        script = header + fields + footer
        return script


    def create_table(self, table_name):
        '''
        One function that takes one of the tuples in a list from table_schemas.py
        '''
        try:
            sqliteConnection = sqlite3.connect(database)
            sqlite_create_query = self.make_create_query(table_name)

            cursor = sqliteConnection.cursor()
            print("Successfully Connected to SQLite")

            # Split the SQL script into individual statements
            sql_statements = sqlite_create_query.split(';')
            for statement in sql_statements:
                if statement.strip():
                    cursor.execute(statement)

            sqliteConnection.commit()
            print(f"{table_name} table created")

            cursor.close()

        except sqlite3.Error as error:
            print("The table creation did not succeed. Error:", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("Make sure you close the connection on the way out")


    def create_all_tables(self):
        '''  
        Orchestrates the creation of the four tables needed in the database for my_spotipy. Should be run as the 
        first act of this application
        '''
        for i in tables:
            self.create_table(i)

    def insert_from_old_db(
            self, 
            table):
        '''
        
        '''
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        old_db = ('my_spotipy.db',)
        attachSQL = ''' ATTACH DATABASE ? AS old_db; '''

        insertSQL = f''' INSERT INTO {table} SELECT * FROM old_db.{table}; '''
        
        cursor.execute(attachSQL, old_db)

        cursor.execute(insertSQL)
        conn.commit()
        conn.close()

    def insert_new_arts(self):
        '''
        OCT10 was the API query date!
        Grabs the newly formated art cat entries made from art_ids found in teh old database
        Inserts these into the artist_catalog table of the new database.
        '''
        ready_for_db = harvest_migration_json('big_migration.json')
        new_insert_query = make_insert_query(
            'artist_catalog',
            [i[0] for i in table_schemas['artist_catalog']]
        )
        conn = sqlite3.connect('fredlambuth.db')
        cursor = conn.cursor()
        cursor.executemany(new_insert_query, ready_for_db)
        conn.commit()
        cursor.close()
        conn.close()

    def insert_track_cats(self):
        with open('tracks_data.json') as holder:
            track_data = json.load(holder)

        keys = list(track_data[0].keys())
        data_list = [list(item[key] for key in keys) for item in track_data]

        new_insert_query = make_insert_query(
            'track_catalog',
            [i[0] for i in table_schemas['track_catalog']]
        )

        conn = sqlite3.connect('fredlambuth.db')
        cursor = conn.cursor()
        cursor.executemany(new_insert_query, data_list)
        conn.commit()
        cursor.close()
        conn.close()

    def initialize(self):
        '''
        Incorporates all the prior functions into one to:
            -create sqlite3 db file
            -create 4 tables based on schema in self.____
            -copies data from spotify.db into newly created db
        '''
        self.create_all_tables()
        tables = ['daily_tracks', 'daily_artists', 'recently_played']
        for i in tables:
            self.insert_from_old_db(i)
            print(f'created {i}')
        self.insert_new_arts()
        self.insert_track_cats()
        print('Database is ready to go!')




###########
def three_genre_fields(genre_list):

    result = genre_list[:3]  # Get the first three elements
    while len(result) < 3:
        result.append(None)  
    return result

def three_img_fields(img_list):

    result = img_list[:3]  
    result = [i['url'][24:] for i in result]

    # Fill with None if needed
    while len(result) < 3:
        result.append(None) 
    return result

def spot_json_to_list(spot_art_record):
    '''
    Given a JSON result from a request to the 'artist' Spotipy API endpoint,
    returns a list of values that match the schema for artist_catalog
    '''
    genres = three_genre_fields(spot_art_record['genres'])
    images = three_img_fields(spot_art_record['images'])

    art_data = [
        spot_art_record['id'],
        spot_art_record['name'],
        spot_art_record['followers']['total'],
        genres[0],
        genres[1],
        genres[2],
        images[0],
        images[1],
        images[2],
    ]
    return art_data

def harvest_migration_json(json_file):

    with open(json_file) as holder:
        big_mig_data = json.load(holder)
        big_mig_parts_list = [spot_json_to_list(i) for i in big_mig_data]
        master_genre = [sublist + [inspect_tri_genres(sublist[3:6])] for sublist in big_mig_parts_list]
        #2023-10-10 was the date the Spotify API records were requested
        ready_for_db = [sublist + ['2023-10-10'] for sublist in master_genre]
    return ready_for_db
#########################
'''
def insert_new_arts():

    ready_for_db = harvest_migration_json('big_migration.json')
    new_insert_query = make_insert_query(
        'artist_catalog',
        [i[0] for i in obj.table_schemas['artist_catalog']]
    )
    conn = sqlite3.connect('fredlambuth.db')
    cursor = conn.cursor()
    conn.commit()
    cursor.close()
    conn.close()
'''
#with open('new_stuff.json') as json_file:
#    new_art_cat_data = json.load(json_file)