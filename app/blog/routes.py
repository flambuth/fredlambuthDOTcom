from app.blog import bp
from app.blog.forms import SearchForm, LoginForm
from app.extensions import db
from app.models.blog import blog_posts, blog_users
from urllib.parse import urlsplit

from sqlalchemy import func, desc
from flask_login import current_user, login_user, logout_user
from flask import render_template, request, redirect, url_for, flash

###########################
#######LOGIN AND LOGOUT
@bp.route('/blog/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.blog_landing_page'))

    form = LoginForm()

    if form.validate_on_submit():
        user = blog_users.query.filter_by(username=form.username.data).first()

        #if there is no users of if the password doesn't check out
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('blog.login'))

        #sets the 'current_user' variable to 'yes'
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('blog.blog_landing_page')

        return redirect(url_for('blog.blog_landing_page'))

    return render_template('blog/blog_login.html', title='Sign In', form=form)


########################################################
@bp.route('/blog/logout', methods=['GET', 'POST'])
def logout():
    
    if request.method == 'POST':
        logout_user()
        flash('You have been logged out.')
        return redirect(url_for('homepage'))

    return render_template('blog/blog_logout.html')

@bp.route('/blog', methods=['GET', 'POST'])
@bp.route('/blog/', methods=['GET', 'POST'])
def blog_landing_page():
    searchform = SearchForm()
    if request.method == 'POST':
        return redirect(url_for('blog.blog_index_search', search_term=searchform.search_term.data))
    latest_6_posts = blog_posts.query.order_by(desc(blog_posts.id)).limit(6).all()

    context = {
        'year_month_index' : blog_posts.year_month_blogpost_index(),
        'latest_6_posts' : latest_6_posts,
        'form':searchform,

    }
    return render_template('blog/blog_landing_page.html', **context)

@bp.route('/blog/<string:year_month>', methods=['GET', 'POST'])
def blog_yearmonth_group(year_month):
    searchform = SearchForm()
    if request.method == 'POST':
        return redirect(url_for('blog.blog_index_search', search_term=searchform.search_term.data))
    posts = blog_posts.query.filter(blog_posts.post_date.like(f'{year_month}%')).all()

    context = {
        'posts' : posts,
        'form':searchform,
    }
    return render_template('blog/blog_index.html', **context)

@bp.route('/blog/post/<int:id>', methods=['GET', 'POST'])
def blog_single(id):
    searchform = SearchForm()
    if request.method == 'POST':
        return redirect(url_for('blog.blog_index_search', search_term=searchform.search_term.data))
    max_id = db.session.query(func.max(blog_posts.id)).all()[0][0]
    if id==max_id:
        next_post=None
    else:
        next_post = blog_posts.query.filter(blog_posts.id==id+1).all()[0]
    post = blog_posts.query.filter(blog_posts.id==id).all()[0]

    if id==1:
        prev_post=None
    else:
        prev_post = blog_posts.query.filter(blog_posts.id==id-1).all()[0]

    context = {
        'post' : post,
        'prev_post' : prev_post,
        'next_post' : next_post,
        'form':searchform,
    }
    return render_template('blog/blog_single.html', **context)

@bp.route('/blog/search/<string:search_term>', methods=('GET','POST'))
def blog_index_search(search_term):
    searchform = SearchForm()
    if request.method == 'POST':
        return redirect(url_for('blog.blog_index_search', search_term=searchform.search_term.data))

    blogs_like = blog_posts.content.like(f"%{search_term}%")
    blog_matches = blog_posts.query.filter(blogs_like).order_by(desc('id')).all()

    context = {
        'posts':blog_matches,
        'form':searchform,
    }

    return render_template('blog/blog_index.html', **context)
