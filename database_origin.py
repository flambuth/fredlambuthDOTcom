import sqlite3
import json

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

    with open('big_migration.json') as json_file:
        big_mig_data = json.load(json_file)
        big_mig_parts_list = [spot_json_to_list(i) for i in big_mig_data]
    return big_mig_parts_list

class Old_Database:
    database = 'my_spotipy.db'
    tables = ['daily_tracks','daily_artists','recently_played','artist_catalog']
    table_schemas = {
            'artist_catalog' : [
                ('art_id', 'TEXT'),
                ('art_name', 'TEXT'),
                ('followers', 'INTEGER'),
                ('genre', 'TEXT'),
                ('first_release', 'TEXT'),
                ('first_appearance', 'datetime'),
                ('img_url', 'TEXT'),
                ('master_genre', 'TEXT')],
            'daily_tracks' :[('position', 'INTEGER'),
                ('art_id', 'TEXT'),
                ('art_name', 'TEXT'),
                ('album_name', 'TEXT'),
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
                ('last_played', 'datetime'),]}
    
    def __init__(self):
        self.woah = 'this whole time I should have been using class variables'

with open('new_stuff.json') as json_file:
    new_art_data = json.load(json_file)