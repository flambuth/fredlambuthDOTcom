from app.extensions import db
from app import login_manager
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash

def convert_to_iso_date(date_string):
    return datetime.strptime(date_string, '%Y-%b-%d').isoformat()[:10]

class blog_posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    content = db.Column(db.Text)
    post_date = db.Column(db.String(20))

    @property
    def iso_date(self):
        return convert_to_iso_date(self.post_date)
    
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
        sorted_data = sorted(result, key=lambda x: datetime.strptime(x[0], '%Y-%b'), reverse=True)
        return sorted_data

    def __repr__(self):
        return f'<Post "{self.title}">'
    
class blog_users(UserMixin, db.Model):
    '''
    hd = blog_users(
    username='Honky_Dave',
    email='dave@hotmail.com',
    password_hash=blog_users.set_password('ladida')
    )

    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    @classmethod
    def set_password(cls, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Configure user loader for LoginManager outside of the model
    @login_manager.user_loader
    def load_user(user_id):
        return blog_users.query.get(user_id)

    def __repr__(self):
        return f'<blog_user: "{self.username}">'