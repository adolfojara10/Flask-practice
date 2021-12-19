from practicar import db, login_manager, app 
from datetime import datetime 
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as serializer

#to get the id of a user. It is a decorator
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#the models for the ddbb
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    #it's going to be hashed
    password = db.Column(db.String(60), nullable=False)
    #for the relationship with the class Posts. the backref argument is retrieve the 
    #information from the author. lazy is to load the data from the ddbb
    posts = db.relationship('Post', backref='author', lazy=True)
    
    
    def get_reset_token(self, expires_seconds=1800):
        s = serializer(app.config['SECRET_KEY'], expires_seconds)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    
    
    @staticmethod
    def verify_reset_token(token):
        s = serializer(app.config['SECRET_KEY'])
        try:
           user_id = s.loads(token)['user_id']            
        except:
            return None
        
        return User.query.get(user_id)
    
    
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
    
    
    