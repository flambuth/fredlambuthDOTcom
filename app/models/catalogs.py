from app.extensions import db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func
#from .main import daily_tracks

Base = declarative_base()

class artist_catalog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    art_id = db.Column(db.String())
    art_name = db.Column(db.String(150))
    followers = db.Column(db.Integer)
    genre = db.Column(db.String(70))
    genre2 = db.Column(db.String(70))
    genre3 = db.Column(db.String(70))
    img_url = db.Column(db.String(150))
    img_url_mid = db.Column(db.String(150))
    img_url_sml = db.Column(db.String(150))
    master_genre = db.Column(db.String(150))
    app_record_date = db.Column(db.String(150))
    is_current = db.Column(db.Boolean)

    #use this one in the views so that there are not duplicates of each artist
    #this will trim it down to the latest record
    @classmethod
    def get_current_records(cls):
        return cls.query.filter_by(is_current=True)
    
    #this one is the archival view of non_current records
    @classmethod
    def get_inactive_records(cls):
        return cls.query.filter(cls.is_current.is_(None)).all()

    @classmethod
    def count_active_records_by_genre(cls):
        '''
        Returns the count of active records for each genre
        '''
        active_genre_counts = db.session.query(
            cls.master_genre,
            func.count().label('Active Records')
        ).filter(
            cls.is_current.is_(True)
        ).group_by(
            cls.master_genre
        ).order_by(
            func.count().desc()
        ).all()
        return active_genre_counts

    def __repr__(self):
        return f'<art_cat_entry "{self.art_name}">'
    

class track_catalog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    art_name = db.Column(db.String(150))
    album_id = db.Column(db.String())
    album_name = db.Column(db.String(150))
    song_id = db.Column(db.String(70))
    song_name = db.Column(db.String(270))
    img_url = db.Column(db.String(150))
    duration = db.Column(db.Integer)
    app_record_date = db.Column(db.String(150))

    def __repr__(self):
        return f'<track_cat_entry "{self.song_name}">'