from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
db_name = "database.db"#define database file

def create_app():#function to create the application
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'COOKIES'
    # configure the database URI for SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'#f makes it evaluated as a string
    db.init_app(app)

    from .views import views#import views and auth blueprints
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')#register blueprints with application
    app.register_blueprint(auth, url_prefix = '/')

    from .models import User, Transaction
    
    with app.app_context():
        db.create_all()

    login_manager=LoginManager()#initialize login manager 
    login_manager.login_view = 'auth.login'#specify login view endpoint
    login_manager.init_app(app)

    @login_manager.user_loader#telling flask what user we're looking for (knows to look at primary key)
    def load_user(id):
        return User.query.get(int(id))


    return app

def create_database(app):#create the database if it doesn't already exist
    if not path.exists('website/'+db_name):
        db.create_all(app=app)
        print('Created database!')