from app.models.catalogs import artist_catalog
from app.models.charts import daily_artists, daily_tracks
from sqlalchemy import func

def art_id_daily_chart_history(input_art_id):
    '''
    Queries the daily_artists and daily_tracks model to find any results.
    '''
    arts_result = daily_artists.query.filter(daily_artists.art_id.ilike(input_art_id)).all()
    tracks_result = daily_tracks.query.filter(daily_tracks.art_id.ilike(input_art_id)).all()
    both = arts_result + tracks_result

    return both