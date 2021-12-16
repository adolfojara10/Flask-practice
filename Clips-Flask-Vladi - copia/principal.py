from datetime import datetime 
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
#to import the forms created in forms.py
from forms import RegistrationForm, LoginForm

#the app is initiated
app = Flask(__name__)

#a secret key so cookies dont modify the session: cmd: import secret -> secret.token_hex(20)
app.config['SECRET_KEY'] = 'ba261cec9a97fa346e7f82d4f460a857bd1bc87d'

#the connection with bbdd: /// -> are a relative path to the current file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#the instance of the ddbb
db = SQLAlchemy(app)

#the models for the ddbb
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    #it's going to be hashed
    password = db.Column(db.String(60), nullable=False)
    #for the relationship with the class Posts. the backref argument is retrieve the 
    #information from the author. lazy is to load the data from the ddbb
    posts = db.relationship('Post', backref='author', lazy=True)
    
    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    #the datetime is for the date in case it wasn't typed
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    
    #the id who made the post
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self) -> str:
        return f"Post('{self.title}', '{self.date_posted}')"
    
    

posts = [
    {
        'author': 'AJ',
        'title':'Post1',
        'content': 'first post content',
        'date':'08/10/2020'
    },
    {
        'author': 'SA',
        'title':'Post2',
        'content': 'SECOND post content',
        'date':'08/10/2021'
    }
]

#para las rutas
@app.route('/')
@app.route('/index')
def indice():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title="about")

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    
    #once the person is registered, we show a message and redirect him to home page
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!',category='success')
        return redirect(url_for('indice'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    #in case login is successful
    if form.validate_on_submit():
        if form.email.data == 'gavilanesadolfo@gmail.com' and form.password.data == '123456':
            flash(f'Successful login!', category='success')
            return redirect(url_for('indice'))
        else:
            flash(f'Unsuccessful login! Please check your credentials', category='danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
