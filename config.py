import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MONGO_URI = 'mongodb://root:example@localhost:27017/security_agency?authSource=admin'
