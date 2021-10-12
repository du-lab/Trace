import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'Y\xd4\xe6\x8c;U\x94@\xfd\x00$\xba;\x95_E'
