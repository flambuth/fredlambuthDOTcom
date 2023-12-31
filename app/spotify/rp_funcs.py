from app.models.charts import recently_played
from app.models.artist_catalog import artist_catalog

from app import db

from sqlalchemy import func
from datetime import datetime, timedelta

def get_timeframe_of_rp_records(
        start_datetime,
        end_datetime
):
    '''
    Accepts the string fromate of '2023-11-15T09:03:02'
    Returns all the rp_records that are inside the start and endpoint.
    '''
    timeframe_of_rps = recently_played.query.filter(
    recently_played.last_played >= start_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
    recently_played.last_played <= end_datetime.strftime('%Y-%m-%dT%H:%M:%S')
    ).all()
    return timeframe_of_rps

def past_24_hrs_rps():
    '''
    Uses get_timeframe_of_rp_records on a 24 hour timeframe that is ends 24 hours from the time the function is called
    '''
    latest_datetime = recently_played.query.order_by(recently_played.id.desc()).first().last_played
    latest_datetime = datetime.strptime(latest_datetime, '%Y-%m-%dT%H:%M:%S')
    start_datetime =  latest_datetime - timedelta(hours=48)
    end_datetime = latest_datetime - timedelta(hours=24)
    rps_from_past24 = get_timeframe_of_rp_records(start_datetime, end_datetime)
    return rps_from_past24

def scan_for_art_cat_awareness():
    '''
    Returns a 2-tuple. Each element is a list. First is art_names found in the past_24_hrs_rps, 
    second are the art_names that do not
    '''
    yesterday_art_names=list(set([i.art_name for i in past_24_hrs_rps()]))
    heard_of_em = artist_catalog.query.filter(artist_catalog.art_name.in_(yesterday_art_names)).all()
    heard_of_em_names = [i.art_name for i in heard_of_em]
    not_heard_of_em_names = [i for i in yesterday_art_names if i not in heard_of_em_names]
    return heard_of_em_names, not_heard_of_em_names

def rp_average_per_day():
    result = db.session.query(
    func.date(recently_played.last_played).label('play_date'),
    func.count().label('record_count')
    ).group_by('play_date').all()
    daily_avg = sum(i[1] for i in result) / len(result) 
    return int(daily_avg)