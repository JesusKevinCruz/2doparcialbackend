import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False  
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:admin@localhost:5432/flask_db'
