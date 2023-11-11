from app.main import bp

@bp.route('/')
def index():
    return "This is an example app. Sock it to me!"
