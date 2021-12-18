from flask_wtf.form import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.simple import BooleanField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from practicar.models import User 
from flask_login import current_user


class RegistrationForm(FlaskForm):
    #DataRequired() = it makes it a mandatory field
    #Length() = the length of the string
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    passwordConfirmation = PasswordField('Password Confirmation', validators=[DataRequired(), EqualTo('password')])
    
    #To submit a form
    submit = SubmitField('Sign up')
    
    #to validate that the fields are unique
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken , choose another one')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken , choose another one')
    
    

class LoginForm(FlaskForm):
      
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    #to close the session after some time
    remember = BooleanField('Remember me')
        
    #To submit a form
    submit = SubmitField('Login')
    
    
class UpdateAccountForm(FlaskForm):
    
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
        
    #To submit a form
    submit = SubmitField('Update')
    
    #to validate that the fields are unique
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken , choose another one')
            
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken , choose another one')