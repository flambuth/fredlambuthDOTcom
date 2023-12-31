from app.spotify import bp
from flask import render_template, request, redirect, url_for
from app.models.charts import recently_played, daily_artists ,daily_tracks

from app.spotify.forms import CourseForm
from app.spotify.rp_funcs import past_24_hrs_rps, scan_for_art_cat_awareness, rp_average_per_day
import app.spotify.daily_funcs as daily_funcs 
import app.spotify.art_cat_funcs as ac_funcs

from datetime import datetime

#YOU CANT HAVE ANYTHING OUTSIDE OF DECORATED ROUTES! Do it somewhere else and import it.
#latest_daily_date = daily_tracks.query.order_by(daily_tracks.id.desc()).first().date
#latest_date_obj = datetime.strptime(latest_daily_date, "%Y-%m-%d").date()

@bp.route('/spotify')
@bp.route('/spotify/')
def spotify_landing_page():
    '''
    I guess this should look flashy and have a menu that offers something the sidebar of the regular Spotify
    views or the art_cat_base do not offer. Or just a very simple menu, but flashier?
    '''
    latest_5 = ac_funcs.latest_art_cats()
    top_5_arts = daily_funcs.top_ever_daily_artists(5)
    top_5_tracks = daily_funcs.top_ever_daily_tracks(5)
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


@bp.route('/spotify/art_cat/', methods=('GET','POST'))
@bp.route('/spotify/art_cat', methods=('GET','POST'))
def art_cat_landing_page():
    form = CourseForm()
    #if form.validate_on_submit():
    if request.method == 'POST':
        return redirect(url_for('spotify.index_by_search', search_term=form.search_term.data))

    thruples = ac_funcs.genre_landing_thruples()

    context = {
        'thruples' : thruples,
        'form':form,
    }

    return render_template('spotify/art_cat/art_cat_landing.html', **context)

@bp.route('/spotify/art_cat/artist/<string:art_id>', methods=('GET','POST'))
def art_cat_profile(art_id):
    form = CourseForm()
    #if form.validate_on_submit():
    if request.method == 'POST':
        return redirect(url_for('spotify.index_by_search', search_term=form.search_term.data))
    
    profile_context = ac_funcs.art_cat_profile(art_id)
    profile_context['form'] = form

    return render_template('spotify/art_cat/art_cat_profile.html', **profile_context)

@bp.route('/spotify/art_cat/<string:letter>', methods=('GET','POST'))
def index_by_letter(letter):
    form = CourseForm()
    #if form.validate_on_submit():
    if request.method == 'POST':
        return redirect(url_for('spotify.index_by_search', search_term=form.search_term.data))
    
    art_cat_index = ac_funcs.all_art_cats_starting_with(letter)
    
    context = {
        'art_cat_index' : art_cat_index,
        'letter' : letter,
        'form':form,
    }

    return render_template('spotify/art_cat/art_cat_index.html', **context)



@bp.route('/spotify/art_cat/genre/<string:master_genre>', methods=('GET','POST'))
@bp.route('/spotify/art_cat/genre', defaults={'master_genre': None}, methods=('GET','POST'))
def index_by_genre(master_genre):
    form = CourseForm()
    #if form.validate_on_submit():
    if request.method == 'POST':
        return redirect(url_for('spotify.index_by_search', search_term=form.search_term.data))
    
    if master_genre in ac_funcs.genres:
        art_cat_index = ac_funcs.all_art_cats_in_master_genre(master_genre)
    
    else:
        art_cat_index = ac_funcs.art_cats_with_this_genre(master_genre)
    context = {
        'genre': master_genre,
        'art_cat_index': art_cat_index,
        'form':form,
    }

    return render_template('spotify/art_cat/art_cat_index.html', **context)

@bp.route('/spotify/search/<string:search_term>', methods=('GET','POST'))
def index_by_search(search_term):
    form = CourseForm()
    if request.method == 'POST':
        return redirect(url_for('spotify.index_by_search', search_term=form.search_term.data))

    like_arts = ac_funcs.art_cat_name_search(search_term)

    context = {
        'like_arts':like_arts,
        'form':form,
    }

    return render_template('spotify/art_cat/art_cat_search.html', **context)




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
    latest_date = daily_funcs.latest_daily_date(daily_tracks) 
    tracks = daily_funcs.latest_daily_chart(daily_tracks)

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
    latest_date = daily_funcs.latest_daily_date(daily_artists)
    arts = daily_funcs.latest_daily_chart(daily_artists)

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
    context = daily_funcs.archive_chart_context(
        daily_tracks,
        date_obj
    )
    return render_template('spotify/archive_chart_tracks.html', **context)

@bp.route('/spotify/daily/artists/<string:year>/<string:month>/<string:day>', methods=('GET','POST'))
def arts_prev(year, month, day):
    date_obj = datetime.strptime(f'{year}-{month}-{day}', "%Y-%m-%d").date()
    context = daily_funcs.archive_chart_context(
        daily_artists,
        date_obj
    )
    return render_template('spotify/archive_chart_artists.html', **context)

