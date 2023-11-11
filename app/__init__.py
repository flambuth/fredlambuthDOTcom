from flask import Flask
from config import Config
from config import SECRET_KEY


def create_app(config_class=Config):
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(config_class)
    app.config['SECRET_KEY'] = SECRET_KEY

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)