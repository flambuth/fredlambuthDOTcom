from app.main import bp
#from app import db
from flask import render_template
from app.models.charts import recently_played, daily_artists ,daily_tracks
#from app.models.artist_catalog import artist_catalog

from app.main.rp_funcs import past_24_hrs_rps, scan_for_art_cat_awareness
from app.main.daily_funcs import latest_daily_date, latest_daily_chart, daily_chart_joined_art_cat, archive_chart_context

#YOU CANT HAVE ANYTHING OUTSIDE OF DECORATED ROUTES! Do it somewhere else and import it.
#latest_daily_date = daily_tracks.query.order_by(daily_tracks.id.desc()).first().date
#latest_date_obj = datetime.strptime(latest_daily_date, "%Y-%m-%d").date()

@bp.route('/')
def homepage():
    return render_template('homepage.html')

@bp.route('/spotify/rp')
@bp.route('/spotify/rp/')
def yesterday():
    '''
    Route to the recent template.
    '''
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

@bp.route('/spotify/daily/tracks')
@bp.route('/spotify/daily/tracks/')
def daily_tracks_stuff():
    latest_date = latest_daily_date(daily_tracks) 
    tracks = latest_daily_chart(daily_tracks)

    year_num = latest_date[:4]
    month_num = latest_date[5:7]
    day_num = latest_date[8:]

    context = {
        'latest_date' : latest_date,
        'tracks' : tracks,
        'year': year_num,
        'month_num' : month_num,
        'day': day_num,
    }

    return render_template('spotify/latest_tracks.html', **context)

@bp.route('/spotify/daily/artists')
@bp.route('/spotify/daily/artists/')
def daily_artists_stuff():
    latest_date = latest_daily_date(daily_artists)
    arts = latest_daily_chart(daily_artists)
    context = {
        'latest_date' : latest_date,
        'artists' : arts
    }

    return render_template('spotify/latest_artists.html', **context)

@bp.route('/spotify/daily/tracks/<string:year>/<string:month>/<string:day>', methods=('GET','POST'))
def tracks_prev(year, month, day):
    context = archive_chart_context(
        daily_tracks,
        year, month, day
    )
    return render_template('spotify/archive_chart.html', **context)

@bp.route('/spotify/daily/artists/<string:year>/<string:month>/<string:day>', methods=('GET','POST'))
def arts_prev(year, month, day):
    context = archive_chart_context(
        daily_artists,
        year, month, day
    )
    return render_template('spotify/archive_chart.html', **context)