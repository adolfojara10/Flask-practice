from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from practicar.config import Config 

#the instance of the ddbb
db = SQLAlchemy()

#to encrypt the password
bcrypt = Bcrypt()

#for the login
login_manager = LoginManager()
#to redirect to the login page in case we want to acces to the account page without being logedin
login_manager.login_view = 'users.login'
#for the message of login
login_manager.login_message_category = 'info'

mail = Mail()
 


def create_app(config_class=Config):
    #the app is initiated
    app = Flask(__name__)

    app.config.from_object(Config)
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    #the import of the blueprints
    from practicar.users.routes import users 
    from practicar.posts.routes import posts
    from practicar.main.routes import main

    app.register_blueprint(users) 
    app.register_blueprint(posts) 
    app.register_blueprint(main) 
    
    return app