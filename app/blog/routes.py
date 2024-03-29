from app.blog import bp
from app.blog.forms import SearchForm, LoginForm, RegistrationForm, CommentForm, SubmitPictureForm, SubmitBlogForm
from app.extensions import db
from app.utils import resize_image
from app.models.blog import blog_posts, blog_users, blog_comments
from app.models.charts import daily_tracks

from werkzeug.exceptions import RequestEntityTooLarge
from operator import attrgetter
from urllib.parse import urlsplit
import random
from datetime import datetime
from werkzeug.utils import secure_filename
#import os

from sqlalchemy import func, desc
from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, request, redirect, url_for, flash, current_app

###########################
#######LOGIN, LOGOUT, Register_new_user
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user_page'))

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

@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    
    if request.method == 'POST':
        logout_user()
        flash('You have been logged out.')
        return redirect(url_for('homepage'))

    return render_template('blog/blog_logout.html')

@bp.route('/account', methods=['GET', 'POST'])
def account():
    '''
    Login or make a new account.
    '''
    return render_template('blog/blog_account_options.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('blog.user_page'))

    form = RegistrationForm()

    if form.validate_on_submit():
        #print("Form data:", form.data)

        # Check if the provided account creation password is correct
        account_creation_password = form.account_creation_password.data
        required_password = current_app.config.get('BLOG_PSWD')

        if account_creation_password != required_password:
            flash('Invalid account creation password.')
            return redirect(url_for('blog.register'))

        # because the auto_increasing id stopped for this table. I dunno why? 2024_02_24
        rando_id = random.randint(100000, 999999)

        if form.profile_picture.data:
            filename = secure_filename(form.username.data + '.' + form.profile_picture.data.filename.rsplit('.', 1)[1].lower())

            # Constructing the final paths
            input_path = '/home/flambuth/fredlambuthDOTcom/app/static/img/user_pics/placeholder.jpg'  # Placeholder file
            output_path = '/home/flambuth/fredlambuthDOTcom/app/static/img/user_pics/' + filename

            #print("Input Path:", input_path)
            #print("Output Path:", output_path)

            # Save and resize the uploaded file
            form.profile_picture.data.save(input_path)
            #print("File saved to input path")

            resize_image(input_path, output_path)
            #print("File resized and saved to output path")

        password_hash = blog_users.set_password(form.password.data)

        new_user = blog_users(
            id=rando_id,
            username=form.username.data,
            email=form.email.data,
            password_hash=password_hash)

        db.session.add(new_user)
        db.session.commit()

        flash('Congratulations, you are now a registered user!')
        # login_user(new_user)  # Automatically log in the new user after registration
        return redirect(url_for('blog.login'))

    return render_template('blog/blog_register.html', title='Register', form=form)

@bp.route('/user')
@bp.route('/user/')
@login_required
def user_page():
    # Retrieve the user's comments from the database
    user_comments = blog_comments.query.filter_by(user_id=current_user.id).all()
    sorted_user_comments = sorted(user_comments, key=attrgetter('post.title'))

    context = {
        'user_comments':sorted_user_comments,
        'current_user_username': current_user.username,
    }

    return render_template('blog/user_page.html', **context)

@bp.route('/user/change_profile_picture', methods=['GET', 'POST'])
def change_profile_picture():
    if not current_user.is_authenticated:
        return redirect(url_for('blog.user_page'))

    form = SubmitPictureForm()

    try:
        if form.validate_on_submit():
            if form.pic_file.data:
                # You can use the current user's username for the filename
                filename = secure_filename(current_user.username + '.' + form.pic_file.data.filename.rsplit('.', 1)[1].lower())

                input_path = '/home/flambuth/fredlambuthDOTcom/app/static/img/user_pics/placeholder.jpg'
                output_path = '/home/flambuth/fredlambuthDOTcom/app/static/img/user_pics/' + filename

                form.pic_file.data.save(input_path)
                resize_image(input_path, output_path)

                # Update the user's profile picture path in the database
                current_user.profile_picture = output_path
                db.session.commit()

                flash('Profile picture updated successfully!')

                return redirect(url_for('blog.user_page'))

    except RequestEntityTooLarge:
        # Handle file size error
        error_message = 'File size is too large. Please choose a smaller file.'
        return render_template('error_page.html', error_message=error_message)

    return render_template('blog/user_change_profile_picture.html', title='Change Profile Picture', form=form)

@bp.route('/user_activity')
@login_required
def comment_activity():
    # Retrieve the user's comments from the database
    #user_comments = blog_comments.query.all()
    #last_five_comments = user_comments[::-1][:5]
    page = request.args.get('page', 1, type=int)
    per_page = 5
    comments = blog_comments.query.order_by(blog_comments.comment_date.desc()).paginate(page=page, per_page=per_page, error_out=False)

    context = {
        'user_comments':comments,
    }

    return render_template('blog/all_users_comments.html', **context)

@bp.route('/users_page')
def all_users_page():
    stats = blog_users.all_user_stats()

    context = {
        'user_stats':stats,
    }
    return render_template('blog/all_users_showcase.html', **context)

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

@bp.route('/blog/post/<int:post_id>', methods=['GET', 'POST'])
def blog_single(post_id):
    searchform = SearchForm()
    if request.method == 'POST':
        return redirect(url_for('blog.blog_index_search', search_term=searchform.search_term.data))
    max_id = db.session.query(func.max(blog_posts.id)).all()[0][0]
    if post_id==max_id:
        next_post=None
    else:
        next_post = blog_posts.query.filter(blog_posts.id==post_id+1).all()[0]
    post = blog_posts.query.filter(blog_posts.id==post_id).all()[0]

    if post_id==1:
        prev_post=None
    else:
        prev_post = blog_posts.query.filter(blog_posts.id==post_id-1).all()[0]

    top_3_songs = daily_tracks.random_n_tracks_that_day(post.iso_date)
    post_comments = blog_comments.query.filter_by(post_id=post_id).all()

    context = {
        'post' : post,
        'prev_post' : prev_post,
        'next_post' : next_post,
        'top_3_songs' : top_3_songs,
        'form':searchform,
        'comments': post_comments,
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
        return redirect(url_for('blog.blog_single', post_id=post_id))

    return render_template('blog/blog_add_comment.html', post=post, form=form)

@bp.route('/upload_blog_post', methods=['GET', 'POST'])
@login_required
def submit_blog_post():
    if current_user.username != 'eddie_from_chicago':
            flash("You are not authorized to access this page.")
            return redirect(url_for('blog.blog_landing_page'))

    form = SubmitBlogForm()
    latest_blog_id = str(blog_posts.last_post_id() + 1)
    test_file_name = f'pic_{latest_blog_id}.jpg'
    filename = secure_filename(test_file_name)
    print(filename)

    
    
    if form.validate_on_submit():

        print("Form data:", form.data)

        # Check if the provided account creation password is correct
        if form.picture.data:

            # Constructing the final paths
            blog_pic_dir = '/home/flambuth/fredlambuthDOTcom/app/static/img/blog_pics/'
            input_path = blog_pic_dir + filename

            print("File to be Saved:", input_path)

            # Save and resize the uploaded file
            form.picture.data.save(input_path)
            print("File saved to input path")

        new_post = blog_posts(
            id = blog_posts.last_post_id() + 1,
            title=form.title.data,
            content=form.content.data,
            post_date=datetime.today().strftime('%Y-%b-%d'))

        db.session.add(new_post)
        db.session.commit()

        # login_user(new_user)  # Automatically log in the new user after registration
        return redirect(url_for('blog.blog_landing_page'))

    else:
        # Form submission failed validation
        # Print validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in field '{field}': {error}")
                print(f"Error in field '{field}': {error}")
        return render_template('blog/blog_add_post.html', title='Register', form=form)