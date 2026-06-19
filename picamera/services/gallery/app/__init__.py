from flask import Flask

app = Flask(__name__)
app.config['PHOTOS_DIRECTORY'] = '/home/pi/camera/photos'
app.config['VIDEOS_DIRECTORY'] = '/home/pi/camera/videos'
app.secret_key = 'supersecretkey'

from app.routes import main

app.register_blueprint(main)