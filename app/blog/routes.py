from app.blog import bp
from app.blog.forms import SearchForm, LoginForm, RegistrationForm, CommentForm
from app.extensions import db
from app.models.blog import blog_posts, blog_users, blog_comments
from app.models.charts import daily_tracks

from urllib.parse import urlsplit
import random
from datetime import datetime

from sqlalchemy import func, desc
from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, request, redirect, url_for, flash, current_app

###########################
#######LOGIN, LOGOUT, Register_new_user
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

        else:
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or urlsplit(next_page).netloc != '':
                next_page = url_for('blog.blog_landing_page')
            return redirect(next_page)

    return render_template('blog/blog_login.html', title='Sign In', form=form)

@bp.route('/blog/logout', methods=['GET', 'POST'])
def logout():
    
    if request.method == 'POST':
        logout_user()
        flash('You have been logged out.')
        return redirect(url_for('homepage'))

    return render_template('blog/blog_logout.html')

@bp.route('/blog/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('blog.blog_landing_page'))

    form = RegistrationForm()

    if form.validate_on_submit():
        print(form.data)
        # Check if the provided account creation password is correct
        account_creation_password = form.account_creation_password.data
        required_password = current_app.config.get('BLOG_PSWD')

        if account_creation_password != required_password:
            flash('Invalid account creation password.')
            return redirect(url_for('blog.register'))

        
        rando_id = random_number = random.randint(100000, 999999)
        password_hash = blog_users.set_password(form.password.data)

        new_user = blog_users(
            id=rando_id,
            username=form.username.data, 
            email=form.email.data, 
            password_hash=password_hash)
        

        db.session.add(new_user)
        db.session.commit()

        flash('Congratulations, you are now a registered user!')
        #login_user(new_user)  # Automatically log in the new user after registration
        return redirect(url_for('blog.login'))

    return render_template('blog/blog_register.html', title='Register', form=form)


#################################################
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

    top_3_songs = daily_tracks.top_n_tracks_that_day(post.iso_date)
    print(top_3_songs)

    context = {
        'post' : post,
        'prev_post' : prev_post,
        'next_post' : next_post,
        'top_3_songs' : top_3_songs,
        'form':searchform,
    }
    return render_template('blog/blog_single.html', **context)

@bp.route('/blog/search/<string:search_term>', methods=('GET','POST'))
@login_required
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



#####################
###comments
@bp.route('/blog/add_comment/<int:post_id>', methods=['GET', 'POST'])
@login_required
def blog_add_comment(post_id):
    form = CommentForm()
    post = blog_posts.query.filter(blog_posts.id==post_id).all()[0]

    if form.validate_on_submit():
        new_comment = blog_comments(
            content=form.content.data,
            post_id=post_id,
            user_id=current_user.id,
            comment_date=datetime.utcnow()
        )

        db.session.add(new_comment)
        db.session.commit()

        flash('Your comment has been added!', 'success')
        return redirect(url_for('blog.blog_single', id=post_id))

    return render_template('blog/blog_add_comment.html', post=post, form=form)