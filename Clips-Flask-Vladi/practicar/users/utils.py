import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from practicar import mail


def savePicture(form_picture):
    
    #to produce a random name for the image so it doesnt repeat
    random_hex = secrets.token_hex(8)
    
    _, f_ext = os.path.splitext(form_picture.filename)
    
    picture_fn = random_hex + f_ext
    
    picture_path = os.path.join(current_app.root_path, 'static/Pics', picture_fn)
    
    #resize image
    output_size = (125,125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
        
    #save image
    img.save(picture_path)
        
    return picture_fn
    
    
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
    
    
