import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://dcarav77:bamsam84@localhost/aa_rmo'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
