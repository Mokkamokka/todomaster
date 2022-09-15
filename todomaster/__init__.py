from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    db_url = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user='postgres', pw='mokka', url='localhost:5432',

                                                                   db='todo_postgres')
    app.config['SECRET_KEY'] = 'my-midnight-super-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from todomaster.services import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_logid(user_id)

    from .views.main import main as main_api
    app.register_blueprint(main_api)

    from .views.auth import auth as auth_api
    app.register_blueprint(auth_api)

    import todomaster.views

    with app.app_context():
        db.create_all()

    return app
