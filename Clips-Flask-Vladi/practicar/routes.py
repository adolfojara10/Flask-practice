from flask import render_template, url_for, flash, redirect, request
from flask_bcrypt import check_password_hash
from practicar.models import User, Post
#to import the forms created in forms.py
from practicar.forms import RegistrationForm, LoginForm
from practicar import app, bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required

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
    
    if current_user.is_authenticated:
        return redirect(url_for('indice'))
    
        
    form = RegistrationForm()
    
    #once the person is registered, we show a message and redirect him to home page
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! You are now able to log in',category='success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('indice'))
    
    form = LoginForm()
    #in case login is successful
    if form.validate_on_submit():
       
       user = User.query.filter_by(email=form.email.data).first()
       
       if user and bcrypt.check_password_hash(user.password, form.password.data):
           login_user(user, remember= form.remember.data)
           #to jump to another page which was tried to go before loged in
           next_page = request.args.get('next')
           
           return redirect(next_page) if next_page else redirect(url_for('indice'))
       else:
           flash(f'Unsuccessful login! Please check your email and password', category='danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('indice'))


@app.route("/account")
@login_required
def account():
    
    return render_template('account.html', title='Account')

