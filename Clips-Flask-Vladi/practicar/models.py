from practicar import db 
from datetime import datetime 

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
    
    
    