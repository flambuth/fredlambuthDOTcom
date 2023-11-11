from data_definition import make_insert_query, query_db
from data_definition import table_schemas, database

from fred_spotify import sp

import sqlite3
import datetime

def check_what_type_is_playing():
    right_now = sp.current_user_playing_track()
    if right_now['currently_playing_type'] == 'track':
        return True


def get_current_track():
    if check_what_type_is_playing():
        right_now = sp.current_user_playing_track()
        
        current_song = right_now['item']
        artist_name = current_song['artists'][0]['name']
        song_name =  current_song['name']
        song_link = current_song['external_urls']['spotify']
        image = current_song['album']['images'][0]['url']
        
        timestamp = right_now['timestamp']/1000
        dt = datetime.datetime.fromtimestamp(timestamp)
        datetime_string = dt.strftime("%Y-%m-%dT%H:%M:%S")

        return {
            'artist_name':artist_name,
            'song_name':song_name,
            'song_link':song_link,
            'image':image,
            'played_at':datetime_string,
        }
    
class Recently_Played:
    def __init__(self):
        self.table = 'recently_played'
        self.col_names = [i[0] for i in  table_schemas[self.table]]
        self.latest_track = query_db('SELECT * FROM recently_played WHERE id = (SELECT MAX(id) FROM recently_played);')[0]
        self.latest_song_id = self.latest_track[3][-22:]

    def check_if_track_is_new(self):
        current_track = get_current_track()
        db_latest_track_id = self.latest_song_id
        if current_track['song_link'][-22:] != db_latest_track_id:
            return current_track
        
    def write_current_track_to_db(self):
        current_track = self.check_if_track_is_new()

        if current_track:
            list_version = [i for i in current_track.values()]
            query = make_insert_query(self.table, self.col_names)
            
            conn = sqlite3.connect(database)
            cursor = conn.cursor()
            cursor.execute(query, list_version)
            conn.commit()
            cursor.close()
            conn.close()

if __name__ == '__main__':
    Recently_Played().write_current_track_to_db()