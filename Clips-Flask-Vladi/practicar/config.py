class Config():
    #a secret key so cookies dont modify the session: cmd: import secret -> secret.token_hex(20)
    SECRET_KEY = 'ba261cec9a97fa346e7f82d4f460a857bd1bc87d'

    #the connection with bbdd: /// -> are a relative path to the current file
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

    #for the email account
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'ajarag2@ieee.org'
    MAIL_PASSWORD = 'adolfocs1'