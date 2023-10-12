import spotipy
from config import username, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        username=username,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI))

def song_id_to_track_cat(song_id):
    '''
    Accepts a song_id, requests the JSON from Spotify, returns a dictionary ready for the track_catalog table
    '''
    hoy_string = datetime.now().today().isoformat()[:10]
    track_record = sp.track(song_id)
    track_dict = {
        'art_name': track_record['album']['artists'][0]['name'],
        'album_id': track_record['album']['artists'][0]['id'],
        'album_name': track_record['album']['name'],
        'song_id' : track_record['id'],
        'song_name' : track_record['name'],
        'img_url' : track_record['album']['images'][0]['url'][24:],
        'duration' : track_record['duration_ms'],
        'app_record_date' : hoy_string,
    }
    return track_dict

#Daily Stuff
def today_top_chart(table_name):
    '''
    Accepts a string of one of the daily tables, requests the short-term top10 from Spotify, returns a JSON
    '''
    if table_name=='daily_artists':
        today_top_results = sp.current_user_top_artists(time_range='short_term', limit=10)
    elif table_name=='daily_tracks':
        today_top_results = sp.current_user_top_tracks(time_range='short_term', limit=10)
    return today_top_results

def JSON_to_listofDicts(
        daily_results_JSON,
        table_name
        ):
    '''
    Parses a JSON that is delivered from either of the two daily type API requests made
    Use *(table_name, raw_JSON) to unpack the tuple from spot_funcs.daily_table
    '''
    hit_list = []
    position = 1

    if table_name == 'daily_artists':

        for i in daily_results_JSON['items']:
            hit_record = {}
            hit_record['position'] = position
            hit_record['art_id'] = i['id']
            hit_record['art_name'] = i['name']
            hit_record['date'] = datetime.now().strftime("%Y-%m-%d")
            
            position += 1
            hit_list.append(hit_record)
    
    if table_name == 'daily_tracks':

        for i in daily_results_JSON['items']:
            hit_record = {}
            hit_record['position'] = position
            hit_record['art_id'] = i['artists'][0]['id']
            hit_record['art_name'] = i['artists'][0]['name']
            hit_record['album_name'] = i['album']['name']
            hit_record['song_id'] = i['external_urls']['spotify'][-22:]
            hit_record['song_name'] = i['name']
            hit_record['date'] = datetime.now().strftime("%Y-%m-%d")
    
            position += 1
            hit_list.append(hit_record)

    return hit_list