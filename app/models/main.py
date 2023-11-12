from app.extensions import db
from sqlalchemy.ext.declarative import declarative_base
#from .artist_catalog import artist_catalog

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
    date = db.Column(db.String(150))
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
    date = db.Column(db.String(150))
    def __repr__(self):
        return f'<daily_artists for "{self.date}">'

class recently_played(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    art_name = db.Column(db.String(150))
    song_name = db.Column(db.String(150))
    song_link = db.Column(db.String(150))
    image = db.Column(db.String(150))
    last_played = db.Column(db.String(150))
    def __repr__(self):
        return f'<recently_played for "{self.last_played}">'
    