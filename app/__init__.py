from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Membuat instance flask
app = Flask(__name__)
# Load Config ke flask
app.config.from_object('config')
# initial integrasi MySql dengan data
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .models import *
from .routes import web_blueprint, api_blueprint

# Register blueprint digunakan untuk mendaftarkan url agar di kenali pada aplikasi
app.register_blueprint(web_blueprint)
app.register_blueprint(api_blueprint, url_prefix='/api')
