from flask import render_template, url_for, flash, redirect, request, abort
from flask_bcrypt import check_password_hash
from practicar.models import User, Post
#to import the forms created in forms.py
from practicar.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from practicar import app, bcrypt, db, mail
from flask_login import login_user, current_user, logout_user, login_required

import secrets
import os 
#to resize image
from PIL import Image 

from flask_mail import Message


#para las rutas
@app.route('/')
@app.route('/index')
def indice():
    posts = Post.query.all()
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


def savePicture(form_picture):
    
    #to produce a random name for the image so it doesnt repeat
    random_hex = secrets.token_hex(8)
    
    _, f_ext = os.path.splitext(form_picture.filename)
    
    picture_fn = random_hex + f_ext
    
    picture_path = os.path.join(app.root_path, 'static/Pics', picture_fn)
    
    #resize image
    output_size = (125,125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
        
    #save image
    img.save(picture_path)
        
    return picture_fn
    

@app.route("/account", methods=['GET','POST'])
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
        return redirect(url_for('account'))
    
    #to put the user data in the form when is logged in
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    image_file = url_for('static', filename="Pics/" + current_user.image_file)
    return render_template('account.html', title='Account', image_file = image_file, form=form)


@app.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():
    
    form = PostForm()
    
    if form.validate_on_submit():
        post = Post(title= form.title.data, content= form.content.data, author = current_user)
        
        db.session.add(post)
        db.session.commit()
        
        flash('Post created!!', category='success')
        
        return redirect(url_for('indice'))
    return render_template('create_post.html', title='New Post', form = form, legend='New Post')



@app.route("/post/<int:post_id>")
def post(post_id):
    
    post = Post.query.get_or_404(post_id)
    
    return render_template('post.html', title=post.title, post = post)


@app.route("/post/<int:post_id>/update", methods=['GET','POST'])
@login_required
def update_post(post_id):
    
    post = Post.query.get_or_404(post_id)
    
    if post.author != current_user:
        abort(403)
    
    form = PostForm()
    
    if form.validate_on_submit():
        post.title = form.title.data 
        post.content = form.content.data 
        
        db.session.commit()
        
        flash("Post updated!!!", category="success")
        
        return redirect(url_for('post', post_id=post.id))
    
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        
        
    return render_template('create_post.html', title="Update Post", post = post, form = form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    
    post = Post.query.get_or_404(post_id)
    
    if post.author != current_user:
        abort(403)
      
    db.session.delete(post)
    db.session.commit()
    
    flash("Post deleted!!!", category="success")
    
    return redirect(url_for('indice'))


def send_reset_email(user):
    token = user.get_reset_token()
    
    msg = Message('Password Reset Request', 
                  sender='noreply@demo.com', 
                  recipients=[user.email],)
    
    msg.body = f'''
To reset your password visit the following link:
{url_for('reset_token', token=token, _external=True)}
        
If you did not make this request, then ignore this email and no changes need to be done
    
'''
    mail.send(msg)

@app.route("/reset_password", methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('indice'))
    
    form = RequestResetForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', category='info')
        return redirect(url_for('login'))
        
    
    return render_template('reset_request.html', title="Reset Password", form = form)


@app.route("/reset_password/<token>", methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('indice'))
    
    user = User.verify_reset_token(token)
    
    if user is None:
        flash('invalid token', category="warning")
        return redirect(url_for('reset_request'))
    
    form = ResetPasswordForm()
    
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw        
        db.session.commit()
        flash(f'Your password has been changed!',category='success')
        return redirect(url_for('login'))
    
    return render_template('reset_token.html', title="Reset Password", form = form)
    
    