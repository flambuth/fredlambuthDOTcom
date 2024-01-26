from app.blog import bp
from app.extensions import db
from app.models.blog import blog_posts

from sqlalchemy import func, desc

from flask import render_template


#YOU CANT HAVE ANYTHING OUTSIDE OF DECORATED ROUTES! Do it somewhere else and import it.
#latest_daily_date = daily_tracks.query.order_by(daily_tracks.id.desc()).first().date
#latest_date_obj = datetime.strptime(latest_daily_date, "%Y-%m-%d").date()

@bp.route('/blog')
@bp.route('/blog/')
def blog_landing_page():

    context = {
        'year_month_index' : blog_posts.year_month_blogpost_index(),
    }
    return render_template('blog/blog_landing_page.html', **context)

@bp.route('/blog/<string:year_month>')
def blog_yearmonth_group(year_month):

    posts = blog_posts.query.filter(blog_posts.post_date.like(f'{year_month}%')).all()

    context = {
        'posts' : posts,
    }
    return render_template('blog/blog_index.html', **context)

@bp.route('/blog/post/<int:id>')
def blog_single(id):
    max_id = db.session.query(func.max(blog_posts.id)).all()[0][0]
    if id==max_id:
        next_post=None
    else:
        next_post = blog_posts.query.filter(blog_posts.id==id+1).all()[0]
    posts = blog_posts.query.filter(blog_posts.id==id).all()

    if id==1:
        prev_post=None
    else:
        prev_post = blog_posts.query.filter(blog_posts.id==id-1).all()[0]

    context = {
        'posts' : posts,
        'prev_post' : prev_post,
        'next_post' : next_post
    }
    return render_template('blog/blog_single.html', **context)
