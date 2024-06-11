import os

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_URL = os.getenv('REDIS_URL')
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY') 