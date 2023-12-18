from app.spotify import bp
from flask import render_template, request
from app.models.charts import recently_played, daily_artists ,daily_tracks

from app.spotify.rp_funcs import past_24_hrs_rps, scan_for_art_cat_awareness, rp_average_per_day
from app.spotify.daily_funcs import latest_daily_date, latest_daily_chart, archive_chart_context, top_ever_daily_artists, top_ever_daily_tracks
from app.spotify.art_cat_funcs import latest_art_cats, all_art_cats_starting_with, all_art_cats_in_master_genre, art_cat_genre_group_counts

from datetime import datetime

#YOU CANT HAVE ANYTHING OUTSIDE OF DECORATED ROUTES! Do it somewhere else and import it.
#latest_daily_date = daily_tracks.query.order_by(daily_tracks.id.desc()).first().date
#latest_date_obj = datetime.strptime(latest_daily_date, "%Y-%m-%d").date()

@bp.route('/spotify')
def spotify_landing_page():

    latest_5 = latest_art_cats()
    top_5_arts = top_ever_daily_artists(5)
    top_5_tracks = top_ever_daily_tracks(5)
    daily_rp_avg = rp_average_per_day()

    context = {
        'latest_artists':latest_5,
        'top_5_arts' : top_5_arts,
        'top_5_tracks' : top_5_tracks,
        'daily_rp_avg' : daily_rp_avg,
    }
    return render_template('spotify/spotify_homepage.html', **context)


###########################################
#art_cat routes


@bp.route('/spotify/art_cat/')
@bp.route('/spotify/art_cat')
def art_cat_landing_page(letter):
    group_counts = art_cat_genre_group_counts()

    context = {
        'group_counts' : group_counts
    }

    return render_template('spotify/art_cat_index.html', **context)

@bp.route('/spotify/art_cat/<string:letter>')
def index_by_letter(letter):
    art_cat_index = all_art_cats_starting_with(letter)
    
    context = {
        'art_cat_index' : art_cat_index
    }

    return render_template('spotify/art_cat/art_cat_index.html', **context)



@bp.route('/spotify/art_cat/genre/<string:master_genre>')
@bp.route('/spotify/art_cat/genre', defaults={'master_genre': None})
def index_by_genre(master_genre):
    art_cat_index = all_art_cats_in_master_genre(master_genre)  

    context = {
        'genre': master_genre,
        'art_cat_index': art_cat_index
    }

    return render_template('spotify/art_cat/art_cat_index.html', **context)


###########################################
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


#############################################
@bp.route('/spotify/daily/tracks')
@bp.route('/spotify/daily/tracks/')
def latest_daily_tracks():
    latest_date = latest_daily_date(daily_tracks) 
    tracks = latest_daily_chart(daily_tracks)

    context = {
        'latest_date' : latest_date,
        'tracks' : tracks,
        'year': latest_date.year,
        'month_num' : latest_date.month,
        'day': latest_date.day,
    }

    return render_template('spotify/latest_tracks.html', **context)

@bp.route('/spotify/daily/artists')
@bp.route('/spotify/daily/artists/')
def latest_daily_artists():
    latest_date = latest_daily_date(daily_artists)
    arts = latest_daily_chart(daily_artists)

    context = {
        'latest_date' : latest_date,
        'artists' : arts,
        'year': latest_date.year,
        'month_num' : latest_date.month,
        'day': latest_date.day,
    }

    return render_template('spotify/latest_artists.html', **context)

@bp.route('/spotify/daily/tracks/<string:year>/<string:month>/<string:day>', methods=('GET','POST'))
def tracks_prev(year, month, day):
    date_obj = datetime.strptime(f'{year}-{month}-{day}', "%Y-%m-%d").date()
    context = archive_chart_context(
        daily_tracks,
        date_obj
    )
    return render_template('spotify/archive_chart_tracks.html', **context)

@bp.route('/spotify/daily/artists/<string:year>/<string:month>/<string:day>', methods=('GET','POST'))
def arts_prev(year, month, day):
    date_obj = datetime.strptime(f'{year}-{month}-{day}', "%Y-%m-%d").date()
    context = archive_chart_context(
        daily_artists,
        date_obj
    )
    return render_template('spotify/archive_chart_artists.html', **context)

