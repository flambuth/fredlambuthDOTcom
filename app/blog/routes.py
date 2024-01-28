from app.blog import bp
from app.blog.forms import CourseForm
from app.extensions import db
from app.models.blog import blog_posts

from sqlalchemy import func, desc

from flask import render_template, request, redirect, url_for


#YOU CANT HAVE ANYTHING OUTSIDE OF DECORATED ROUTES! Do it somewhere else and import it.
#latest_daily_date = daily_tracks.query.order_by(daily_tracks.id.desc()).first().date
#latest_date_obj = datetime.strptime(latest_daily_date, "%Y-%m-%d").date()

@bp.route('/blog')
@bp.route('/blog/')
def blog_landing_page():

    latest_6_posts = blog_posts.query.order_by(desc(blog_posts.id)).limit(6).all()

    context = {
        'year_month_index' : blog_posts.year_month_blogpost_index(),
        'latest_6_posts' : latest_6_posts,
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

@bp.route('/blog/search/<string:search_term>', methods=('GET','POST'))
def blog_index_search(search_term):
    form = CourseForm()
    if request.method == 'POST':
        return redirect(url_for('blog.blog_index_search', search_term=form.search_term.data))

    blogs_like = blog_posts.content.like(f"%{search_term}%")
    blog_matches = blog_posts.query.filter(blogs_like).order_by(desc('id')).all()

    context = {
        'blog_matches':blog_matches,
        'form':form,
    }

    return render_template('blog/blog_search.html', **context)
