from app.extensions import db
from sqlalchemy.ext.declarative import declarative_base
#from .main import daily_tracks

Base = declarative_base()

class artist_catalog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    art_id = db.Column(db.String())
#    art_id = db.relationship(
#        'daily_tracks',
#        backref='artist_cat',
#        lazy=True    )
    art_name = db.Column(db.String(150))
    followers = db.Column(db.Integer)
    genre = db.Column(db.String(70))
    first_release = db.Column(db.String(150))
    first_appearance = db.Column(db.String(150))
    img_url = db.Column(db.String(150))
    master_genre = db.Column(db.String(150))

    def __repr__(self):
        return f'<art_cat_entry "{self.art_name}">'