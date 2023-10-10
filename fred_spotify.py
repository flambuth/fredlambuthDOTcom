import spotipy
from config import username, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
from spotipy.oauth2 import SpotifyOAuth

class Spotify_Request:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        username=username,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI))

    def __init__(self):
        self.blah = 'blah blah'

    def get_artist_info(self, art_id):             
        '''
        Processes one art_id at a time
        Returns a dictionary. Keys are the columns in artist table. Only one value per key. 

        '''
        artist = self.sp.artist(art_id)
        albums = self.sp.artist_albums(art_id)

        art_name = artist['name']
        followers = artist['followers']['total']
        if len(artist['genres']) == 0:
            genre = 'None'
        else:
            genre = artist['genres'][0]

        first_release = min([i['release_date'] for i in albums['items']])
        if artist['images']:
            img_url = artist['images'][0]['url']
        else:
            img_url = 'no_image'
        #master_genre = Genres.Genres().new_artist_master_genre(genre)
        #needs master_genre and first_appearance
        new_artist_values = [art_id, art_name, followers, genre, first_release, img_url]
        return new_artist_values