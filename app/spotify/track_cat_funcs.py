from app.models.catalogs import track_catalog

def all_tracks_starting_with(letter):
    
    start_with_letter = track_catalog.query.filter(
        track_catalog.song_name.startswith(letter)
            ).order_by('song_name').all()
    
    track_letter_results = start_with_letter
    return track_letter_results