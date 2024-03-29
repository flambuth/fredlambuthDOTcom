from app.extensions import db
from app import login_manager
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash

def convert_to_iso_date(date_string):
    return datetime.strptime(date_string, '%Y-%b-%d').isoformat()[:10]

class blog_posts(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(150))
    content = db.Column(db.Text)
    post_date = db.Column(db.String(20))

    @property
    def iso_date(self):
        return convert_to_iso_date(self.post_date)
    
    @classmethod
    def last_post_id(cls):
        last_id = cls.query.with_entities(cls.id).all()[-1][0]
        return last_id

    @classmethod
    def year_month_blogpost_index(cls):
        result = (
            db.session.query(
                func.substr(cls.post_date, 1, 8).label('year_month'),
                func.count().label('post_count')
            )
            .group_by('year_month')
            .order_by('year_month')  # Optional: Order the results by year-month
            .all()
        )

        #does a quick sort by changing the 2023-JAN string to a measurable date 
        datetime_result = [(datetime.strptime(i[0], '%Y-%b'),i[1]) for i in result]
        sorted_data = sorted(datetime_result, key=lambda x: x[0])
        sorted_strings = [(datetime.strftime(date_str, "%Y-%b"), post_count) for date_str, post_count in sorted_data]
        return sorted_strings

    def __repr__(self):
        return f'<Post "{self.title}">'
    
class blog_users(UserMixin, db.Model):
    '''

    '''
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    #User stats
    @classmethod
    def blog_user_stats(cls, blog_user_id):
        blog_user_comments = blog_comments.query.filter(blog_comments.user_id == blog_user_id).all()
        if blog_user_comments:
            comment_count = len(blog_user_comments)
            start_date = blog_user_comments[0].comment_date.isoformat()[:10]
        else:
            comment_count = 0
            start_date = datetime.now().isoformat()[:10]
        return comment_count, start_date

    @classmethod
    def all_user_stats(cls):
        users = cls.query.with_entities(cls.id, cls.username).all()
        users_ids = [i[0] for i in users]
        users_names = [i[1] for i in users]
        user_stats = list(map(
            cls.blog_user_stats,
            users_ids
        ))
        user_stats = list(zip(users_names, user_stats))
        return user_stats

    #PASSWORD STUFF
    @classmethod
    def set_password(cls, password):
        return generate_password_hash(password)

    @classmethod
    def change_password(cls, username, new_password):
        user = cls.query.filter_by(username=username).first()

        if user:
            # Set the new hashed password
            user.password_hash = cls.set_password(new_password)

            # Commit the changes to the database
            db.session.commit()

            return True  # Password changed successfully
        else:
            return False  # User not found

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Configure user loader for LoginManager outside of the model
    @login_manager.user_loader
    def load_user(user_id):
        return blog_users.query.get(user_id)

    def __repr__(self):
        return f'<blog_user: "{self.username}">'
    


class blog_comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('blog_users.id'), nullable=False)

    post = db.relationship('blog_posts', backref=db.backref('comments', lazy=True))
    user = db.relationship('blog_users', backref=db.backref('comments', lazy=True))
    
    comment_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Comment by {self.user.username} on post "{self.post.title}">'
