import fred_spotify as f_spot
from datetime import datetime
from data_definition import make_insert_query, save_to_db
from data_definition import table_schemas


def my_playlist_list():
    '''
    Makes call to Spotify API to return a tuples of the names and playlist_ids of my user_created
    playlists on Spotify
    '''
    playlist_jsons = f_spot.sp.user_playlists('lambuth')
    my_playlist_jsons = [i for i in playlist_jsons['items'] if i['owner']['id']=='lambuth']
    name_id_tuples = [(i['name'],i['id']) for i in
    my_playlist_jsons]
    return name_id_tuples

dt_pattern = '%Y-%m-%dT%H:%M:%SZ'

class Playlist:
    ''''
    Accepts a tuple from my_playlist_list as parameters to instantiate a playlist object
    '''
    def __init__(self, playlist_name, playlist_id):
        self.table = 'playlists'
        self.col_names = [i[0] for i in  table_schemas[self.table]]

        self.name = playlist_name
        self.playlist_id = playlist_id
        self.json = f_spot.sp.playlist_tracks(playlist_id)#['items']
        self.tracks = self.json['items']
        self.chronology = [i['added_at'] for i in self.tracks]
        self.start_dt =  datetime.strptime(self.chronology[0], dt_pattern)
        self.end_dt = datetime.strptime(self.chronology[-1], dt_pattern)
        self.day_length = (self.end_dt - self.start_dt).days
        
    def get_tracks_records(self):
        track_ids = [(
            self.name,
            self.playlist_id,
            i['track']['id'],
            i['track']['name'],
            i['track']['artists'][0]['id'],
            i['track']['artists'][0]['name'],
            #converts it to seconds
            i['track']['duration_ms']/1000,
            #slices of the Z at the end of this isostring
            i['added_at'][:-1]
        ) for i in self.tracks
        ]
        return track_ids
    
    def write_playlist_to_table(self):
        '''
        table in the database defined in my_spotify/data_definition
        '''
        records = self.get_tracks_records()
        query = make_insert_query(self.table, self.col_names)
        save_to_db(
            query,
            records
        )
        return 'Orale!'
    
def migrate_playlists_to_db():
    '''
    these_tuples are the playlist_name, id tuples is the iterable
    iterator is the Playlist object constructor and write to table method


    '''
    these_tuples = my_playlist_list()[:-2]
    for playlist_tuple in these_tuples:
        Playlist(*playlist_tuple).write_playlist_to_table()
    print('All Playlist Records Inserted!')