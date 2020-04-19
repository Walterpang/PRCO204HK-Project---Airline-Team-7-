import os

class Config:
    pjdir = os.path.abspath(os.path.dirname(__file__))
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:adminadmin@localhost/airline'
    SECRET_KEY = b'\xb9k\xdf@\x0e\x1f(\xf2\xb0\xd0\xcb?Y\xdcN\x19G\x12e\xa8\x8b\xe5\xccS'
    SESSION_PROTECTION = 'strong'
    MAIL_SERVER = 'smtp.office365.com'
    MAIL_PROT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'Your Mail Count'
    MAIL_PASSWORD = 'Your Mail Password'