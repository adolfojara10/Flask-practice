from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from practicar import db, bcrypt
from practicar.models import User, Post
from practicar.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from practicar.users.utils import savePicture, send_reset_email


users = Blueprint('users', __name__)



@users.route('/register', methods=['GET','POST'])
def register():
    
    if current_user.is_authenticated:
        return redirect(url_for('main.indice'))
    
        
    form = RegistrationForm()
    
    #once the person is registered, we show a message and redirect him to home page
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! You are now able to log in',category='success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.indice'))
    
    form = LoginForm()
    #in case login is successful
    if form.validate_on_submit():
       
       user = User.query.filter_by(email=form.email.data).first()
       
       if user and bcrypt.check_password_hash(user.password, form.password.data):
           login_user(user, remember= form.remember.data)
           #to jump to another page which was tried to go before loged in
           next_page = request.args.get('next')
           
           return redirect(next_page) if next_page else redirect(url_for('main.indice'))
       else:
           flash(f'Unsuccessful login! Please check your email and password', category='danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.indice'))


@users.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        
        if form.picture.data:
            picture_file = savePicture(form.picture.data)
            current_user.image_file = picture_file
            
        current_user.username = form.username.data 
        current_user.email = form.email.data 
        
        db.session.commit()
        flash('Your account has been updated', category="success")
        return redirect(url_for('users.account'))
    
    #to put the user data in the form when is logged in
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    image_file = url_for('static', filename="Pics/" + current_user.image_file)
    return render_template('account.html', title='Account', image_file = image_file, form=form)


@users.route("/reset_password", methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.indice'))
    
    form = RequestResetForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', category='info')
        return redirect(url_for('users.login'))
        
    
    return render_template('reset_request.html', title="Reset Password", form = form)


@users.route("/reset_password/<token>", methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.indice'))
    
    user = User.verify_reset_token(token)
    
    if user is None:
        flash('invalid token', category="warning")
        return redirect(url_for('users.reset_request'))
    
    form = ResetPasswordForm()
    
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw        
        db.session.commit()
        flash(f'Your password has been changed!',category='success')
        return redirect(url_for('users.login'))
    
    return render_template('reset_token.html', title="Reset Password", form = form)
    