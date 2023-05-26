from flask import Blueprint
from ..controllers import mainController

web_blueprint = Blueprint('web', __name__)

web_blueprint.route('/', methods=['GET'])(mainController.index)
web_blueprint.route('/predict', methods=['GET'])(mainController.prediction)