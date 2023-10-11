import sqlite3

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

class DB_Table:
    '''
    This is an abstract table that should not be ever instatiated. I mean you could, but
    that would be sorta useless.
    '''
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
                ('genre1', 'TEXT'),
				('genre2', 'TEXT'),
				('genre3', 'TEXT'),
                ('img_url', 'TEXT'),
				('img_url_mid', 'TEXT'),
				('img_url_sml', 'TEXT'),
                ('master_genre', 'TEXT'),
				('record_date', 'datetime'),],
                
            'track_catalog' : [
                ('art_name', 'TEXT'),
                ('album_id', 'TEXT'),
                ('album_name', 'TEXT'),
                ('song_id', 'TEXT'),
                ('song_name', 'TEXT'),
                ('first_appearance', 'datetime'),
                ('img_url', 'TEXT'),],


            'daily_tracks' :[('position', 'INTEGER'),
                ('art_id', 'TEXT'),
                ('album_id', 'TEXT'),
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

    def __init__(self, table):
        self.table = table
        self.schema = self.table_schemas[table]
        self.col_names = [i[0] for i in self.schema]
        self.d_types = [i[1] for i in self.schema]

    def query_db(self, query):
        '''
        Returns a set of .fetchall() restults from the db

        YOU NEED TO MIGRATE BEFORE THIS CAN WORK! (july 16,2022)
        '''
        try:
            conn = sqlite3.connect(self.database)
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

    def make_insert_query(self):
        '''
        Creates a SQLite3 friendly insert statement that can fit on any of the 4 tables stashed as an object variable.
        '''
        marks = make_question_marks(self.col_names)
        col_string = ','.join(self.col_names)
        insert_sql = f'''INSERT INTO {self.table} ({col_string}) VALUES ({marks}) '''
        return insert_sql
    
    
class Daily_Table(DB_Table):
    def __init__(self, table):
        super().__init__(table)
        self.latest_date = self.query_db(f'select MAX(date) from {self.table}')[0][0]
        #self.all_charts = self.query_db(f'select * from {table};')
        #self.art_names_in_charts = sorted(list(set([i[3] for i in self.all_charts])))

    def fetch_latest_chart(self):
        '''
        Returns the latest chart in the list_of_tuples format that sqlite3 spits out
        '''
        query = f'select * from {self.table} ORDER BY id DESC LIMIT 10;'
        results = self.query_db(query)
        return results

    def traffic_check(self, new_daily):
        '''
        Compares the date of the 'new_daily' chart to make sure it is later than
        the most recent date of the daily table it is being appended to
        '''
        if self.latest_date < new_daily[0]['date']:
            return True

    def flatten_daily_to_list(self, new_daily):
        '''
        Converts the dictionary into a list of lists. 
        Each list has same length. 
        Each list is a 'column' each index is a 'row'
        '''
        list_version = [list(i.values()) for i in new_daily]
        return list_version

    def insert_new_daily(self, new_daily):
        '''
        the new_daily should be a Spotifies.daily_insert.daily_book
        '''
        #new_date = new_daily[0]['date']
        sql = self.make_insert_query(self.table, self.col_names)

        if self.traffic_check(new_daily):
            sqliteConnection = sqlite3.connect(self.database)
            cursor = sqliteConnection.cursor()
            #executemany takes a lists of lists, not the usualy dictionary of lists
            flat_daily = self.flatten_daily_to_list(new_daily)
            cursor.executemany(sql, flat_daily)
                
            sqliteConnection.commit()
            cursor.close()
            sqliteConnection.close()

        else:
            print('Failed Traffic Stop')

        print(f'{self.table} has been updated to {self.latest_date}')

tracks = Daily_Table('daily_tracks')
artists = Daily_Table('daily_artists')