from flask import Flask, render_template
from config import Config
from config import SECRET_KEY

from app.extensions import db

def create_app(config_class=Config):
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(config_class)
    app.config['SECRET_KEY'] = SECRET_KEY
    #app.config['SERVER_NAME'] = 'localhost:5000'


    db.init_app(app)

    from app.spotify import bp as main_bp
    app.register_blueprint(main_bp)

    from app.blog import bp as blog_bp
    app.register_blueprint(blog_bp)

    @app.route('/')
    def homepage():
        return render_template('homepage.html')

    @app.route('/contact')
    def contact():
        return render_template('contact.html')

    #from app.dash_plotlys.artist_history import Add_Dash_art_cat
    #Add_Dash_art_cat(app)
    #with app.app_context():
    from app.dash_plotlys.year_month_line_chart import Add_Dash_year_month
    Add_Dash_year_month(app)
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)