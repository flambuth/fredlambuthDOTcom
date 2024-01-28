from app.extensions import db
from datetime import datetime

from sqlalchemy import func

def convert_to_iso_date(date_string):
    return datetime.strptime(date_string, '%Y-%b-%d').isoformat()

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