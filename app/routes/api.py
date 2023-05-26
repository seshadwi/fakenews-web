from flask import Blueprint
from ..controllers import apiController
api_blueprint = Blueprint('api', __name__)


api_blueprint.route('/', methods=['GET'])(apiController.indentify)