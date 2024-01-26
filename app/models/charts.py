from app.extensions import db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func

from datetime import datetime, timedelta

from app.models.catalogs import artist_catalog

Base = declarative_base()

class daily_tracks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer)
    #art_id = db.Column(db.String(23))
    art_id = db.Column(
        db.String(23),
        db.ForeignKey('artist_catalog.id'),
        nullable=False)
    art_name = db.Column(db.String(150))
    album_name = db.Column(db.String(150))
    song_id = db.Column(db.String(23))
    song_name = db.Column(db.String(150))
    date = db.Column(db.Date, nullable=False)
    def __repr__(self):
        return f'<daily_tracks for "{self.date}">'

class daily_artists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer)
    art_id = db.Column(
        db.String(23),
        db.ForeignKey('artist_catalog.id'),
        nullable=False
    )
    art_name = db.Column(db.String(150))
    date = db.Column(db.Date(), nullable=False)
    def __repr__(self):
        return f'<daily_artists for "{self.date}">'

class recently_played(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    art_name = db.Column(db.String(150))
    song_name = db.Column(db.String(150))
    song_link = db.Column(db.String(150))
    image = db.Column(db.String(150))
    last_played = db.Column(db.String(50))

    @classmethod
    def get_timeframe_of_rp_records(
        cls,
            start_datetime,
            end_datetime
    ):
        '''
        Accepts the string fromate of '2023-11-15T09:03:02'
        Returns all the rp_records that are inside the start and endpoint.
        '''
        timeframe_of_rps = cls.query.filter(
        cls.last_played >= start_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
        cls.last_played <= end_datetime.strftime('%Y-%m-%dT%H:%M:%S')
        ).all()
        return timeframe_of_rps
    
    @classmethod
    def past_24_hrs_rps(cls):
        '''
        Uses get_timeframe_of_rp_records on a 24 hour timeframe that is ends 24 hours from the time the function is called
        '''
        latest_datetime = cls.query.order_by(cls.id.desc()).first().last_played
        latest_datetime = datetime.strptime(latest_datetime, '%Y-%m-%dT%H:%M:%S')
        start_datetime =  latest_datetime - timedelta(hours=48)
        end_datetime = latest_datetime - timedelta(hours=24)
        rps_from_past24 = cls.get_timeframe_of_rp_records(start_datetime, end_datetime)
        return rps_from_past24
    
    @classmethod
    def scan_for_art_cat_awareness(cls):
        '''
        Returns a 2-tuple. Each element is a list. First is art_names found in the past_24_hrs_rps, 
        second are the art_names that do not
        '''
        yesterday_art_names=list(set([i.art_name for i in cls.past_24_hrs_rps()]))
        heard_of_em = artist_catalog.query.filter(artist_catalog.art_name.in_(yesterday_art_names)).all()
        heard_of_em_names = list(set([i.art_name for i in heard_of_em]))
        not_heard_of_em_names = list(set([i for i in yesterday_art_names if i not in heard_of_em_names]))
        return heard_of_em_names, not_heard_of_em_names

    @classmethod
    def rp_average_per_day(cls):
        result = db.session.query(
        func.date(cls.last_played).label('play_date'),
        func.count().label('record_count')
        ).group_by('play_date').all()
        daily_avg = sum(i[1] for i in result) / len(result) 
        return int(daily_avg)

    def __repr__(self):
        return f'<recently_played for "{self.last_played}">'
    