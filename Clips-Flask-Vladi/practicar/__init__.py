from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


#the app is initiated
app = Flask(__name__)

#a secret key so cookies dont modify the session: cmd: import secret -> secret.token_hex(20)
app.config['SECRET_KEY'] = 'ba261cec9a97fa346e7f82d4f460a857bd1bc87d'

#the connection with bbdd: /// -> are a relative path to the current file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#the instance of the ddbb
db = SQLAlchemy(app)

#to encrypt the password
bcrypt = Bcrypt(app)

#for the login
login_manager = LoginManager(app)
#to redirect to the login page in case we want to acces to the account page without being logedin
login_manager.login_view = 'login'
#for the message of login
login_manager.login_message_category = 'info'


#the import of the routes
from practicar import routes 