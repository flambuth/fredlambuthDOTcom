from app.main import bp
#from app import db
from flask import render_template
from app.models.charts import recently_played, daily_artists ,daily_tracks
from app.models.artist_catalog import artist_catalog

from datetime import datetime, timedelta, date


#YOU CANT HAVE ANYTHING OUTSIDE OF DECORATED ROUTES! Do it somewhere else and import it.
#latest_daily_date = daily_tracks.query.order_by(daily_tracks.id.desc()).first().date
#latest_date_obj = datetime.strptime(latest_daily_date, "%Y-%m-%d").date()


@bp.route('/')
def homepage():
    return render_template('homepage.html')

@bp.route('/rp')
def recent_stuff():
    three_ago = recently_played.query.all()[-3:]
    #rps_since_last_daily = recently_played.query.filter(db.func.date(recently_played.last_played) == latest_date_obj).all()


    context = {
        'last_three' : three_ago,
        #'traffic_count' : str(len(rps_since_last_daily))
    }

    return render_template('spotify/recently_played.html', **context)

@bp.route('/daily/tracks')
def daily_tracks_stuff():
    latest_daily_date = daily_tracks.query.order_by(daily_tracks.id.desc()).first().date

    tracks = daily_tracks.query.filter(
        daily_tracks.date == latest_daily_date
        ).join(artist_catalog, daily_tracks.art_id==artist_catalog.art_id
        ).add_columns(
            artist_catalog.genre,
            artist_catalog.genre2, 
            artist_catalog.master_genre, 
            artist_catalog.img_url_sml)


    context = {
        'latest_date' : latest_daily_date,
        'tracks' : tracks,
    }

    return render_template('spotify/latest_tracks.html', **context)

@bp.route('/daily/artists')
def daily_artists_stuff():
    latest_daily_date = daily_artists.query.order_by(daily_artists.id.desc()).first().date

    arts = daily_artists.query.filter(
        daily_artists.date == latest_daily_date
        ).join(artist_catalog, daily_artists.art_id==artist_catalog.art_id
        ).add_columns(
            artist_catalog.genre,
            artist_catalog.genre2, 
            artist_catalog.master_genre, 
            artist_catalog.img_url_sml)



    context = {
        'latest_date' : latest_daily_date,
        'artists' : arts
    }

    return render_template('spotify/latest_artists.html', **context)