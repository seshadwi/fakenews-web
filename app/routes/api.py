from flask import Blueprint
from ..controllers import apiController
api_blueprint = Blueprint('api', __name__)


api_blueprint.route('/identify', methods=['GET', 'POST'])(apiController.identify)
api_blueprint.route('/syncnews', methods=['GET', 'POST'])(apiController.syncNews)