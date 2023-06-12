from flask import Blueprint
from ..controllers import mainController

web_blueprint = Blueprint('web', __name__)

web_blueprint.route('/', methods=['GET'])(mainController.index)
web_blueprint.route('/predict', methods=['GET'])(mainController.prediction)
web_blueprint.route('/predict/result/<id>', methods=['GET'])(mainController.details)
web_blueprint.route('/predict/result/<id>/details', methods=['GET'])(mainController.detailSrap)