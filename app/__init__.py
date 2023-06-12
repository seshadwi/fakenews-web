from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .models import *
from .routes import web_blueprint, api_blueprint

app.register_blueprint(web_blueprint)
app.register_blueprint(api_blueprint, url_prefix='/api')
