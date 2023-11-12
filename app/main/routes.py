from app.main import bp
from flask import render_template
from app.models.main import recently_played

@bp.route('/')
def homepage():
    return render_template('homepage.html')

@bp.route('/rp')
def recent_stuff():
    three_ago = recently_played.query.all()[-3:]

    context = {
        'last_three' : three_ago,
    }

    return render_template('recently_played.html', **context)
