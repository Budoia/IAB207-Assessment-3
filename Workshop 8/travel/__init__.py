#import flask - from the package import a module
from flask import Flask 
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db=SQLAlchemy()

#create a function that creates a web application
# a web server will run this web application
def create_app():
    app=Flask(__name__)  # this is the name of the module/package that is calling this app
    app.secret_key='doesnotmatter'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel123.sqlite'
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'aut.login'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    bootstrap = Bootstrap(app)

    from . import views
    app.register_blueprint(views.mainbp)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import destinations
    app.register_blueprint(destinations.bp)

    return app
