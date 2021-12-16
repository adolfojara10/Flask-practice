from flask import render_template, url_for, flash, redirect
from practicar.models import User, Post
#to import the forms created in forms.py
from practicar.forms import RegistrationForm, LoginForm
from practicar import app 

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
