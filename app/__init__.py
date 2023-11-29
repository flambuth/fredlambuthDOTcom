from flask import Flask, render_template
from config import Config
from config import SECRET_KEY

from app.extensions import db

def create_app(config_class=Config):
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(config_class)
    app.config['SECRET_KEY'] = SECRET_KEY

    db.init_app(app)

    from app.spotify import bp as main_bp
    app.register_blueprint(main_bp)

    @app.route('/')
    def homepage():
        return render_template('homepage.html')

    @app.route('/contact')
    def contact():
        return render_template('contact.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)