from app.main import bp
#from app import db
from flask import render_template
from app.models.charts import recently_played, daily_artists ,daily_tracks
from app.models.artist_catalog import artist_catalog

from app.main.rp_funcs import past_24_hrs_rps, scan_for_art_cat_awareness


#YOU CANT HAVE ANYTHING OUTSIDE OF DECORATED ROUTES! Do it somewhere else and import it.
#latest_daily_date = daily_tracks.query.order_by(daily_tracks.id.desc()).first().date
#latest_date_obj = datetime.strptime(latest_daily_date, "%Y-%m-%d").date()


@bp.route('/')
def homepage():
    return render_template('homepage.html')

@bp.route('/rp')
def yesterday():
    three_ago = recently_played.query.all()[-3:]
    yesterday_records = past_24_hrs_rps()
    song_count_yesterday = len(yesterday_records)
    distinct_arts = len(list(set([i.art_name for i in yesterday_records])))
    known, unknown = scan_for_art_cat_awareness()


    context = {
        'last_three' : three_ago,
        'yesterday_song_count' : song_count_yesterday,
        'distinct_arts' : distinct_arts,
        'known':known,
        'unknown':unknown,
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