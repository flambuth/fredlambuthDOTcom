from app.models.charts import daily_artists, daily_tracks
from app.models.artist_catalog import artist_catalog
from app import db

from sqlalchemy import func
from datetime import timedelta

def daily_chart_joined_art_cat(
        chart_model,
        chart_date_obj,
        ):
    '''
    attaches genre and image data from the art_cat table to the daily chart
    '''
    results = chart_model.query.filter(
        chart_model.date == chart_date_obj
        ).outerjoin(artist_catalog, chart_model.art_id==artist_catalog.art_id
        ).add_columns(
            artist_catalog.genre,
            artist_catalog.genre2, 
            artist_catalog.master_genre, 
            artist_catalog.img_url_sml)
    return results

def latest_daily_date(chart_model):
    '''
    Returns a date object for the row with the largest ID
    '''
    latest_date = chart_model.query.order_by(chart_model.id.desc()).first().date
    return latest_date

def latest_daily_chart(chart_model):
    '''
    Uses the latest_daily_date to filter the rows that have the same date. SHould be 10 per daily_type 
    '''
    latest_date = latest_daily_date(chart_model)

    tracks = daily_chart_joined_art_cat(
        chart_model,
        latest_date
        )
    return tracks

def archive_chart_context(
        chart_model,
        date_obj):

    records = daily_chart_joined_art_cat(
        chart_model,
        date_obj
    )
    if not records:
        # Custom message when no data is found
        return "No data found for the specified date."
    
    if chart_model == daily_tracks:
        chart_type = 'Tracks'
    elif chart_model == daily_artists:
        chart_type = 'Artists'
    else:
        chart_type = None

    context = {
        'chart_type' : chart_type,
        'records' : records,
        'date_obj' : date_obj,
        'date_back_1month' : date_obj - timedelta(days=28),
        'date_back_1day' : date_obj - timedelta(days=1),
        'date_fwd_1month' : date_obj + timedelta(days=28),
        'date_fwd_1day' : date_obj + timedelta(days=1),
    }
    return context

def top_ever_daily_artists(
        num=10):
    cream = db.session.query(
    daily_artists.art_name,
    func.count().label('Chart Days')
    ).group_by(daily_artists.art_name
    ).order_by(func.count().desc()
    ).limit(num).all()
    return cream

def top_ever_daily_tracks(
        num=10):
    cream = db.session.query(
    daily_tracks.song_name,
    func.count().label('Chart Days')
    ).group_by(daily_tracks.song_name
    ).order_by(func.count().desc()
    ).limit(num).all()
    return cream