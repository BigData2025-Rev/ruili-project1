import os
from flask_cors import CORS
from flask import Flask
from config.config import Config
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/img'
MAX_CONTENT_LENGTH = 1 * 1024 * 1024  # 1MB

app = Flask(
    __name__,
    template_folder='templates',  
    static_folder='static'        
)
CORS(app) # allow cors request, otherwise I cannot access any non-static request
app.config['SECRET_KEY'] = Config.AppSecretKey  
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
