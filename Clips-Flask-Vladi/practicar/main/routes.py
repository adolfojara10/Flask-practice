from flask import Blueprint, render_template, request
from practicar.models import Post


main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
def indice():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@main.route('/about')
def about():
    return render_template('about.html', title="about")
    