from flask import Blueprint
from ..controllers import mainController

# Digunakan untuk initial blueprint (Routes) yang akan digunakan
web_blueprint = Blueprint('web', __name__)

# Menentukan controller mana yang akan ditampilkan pada url yang sudah di tentukan
web_blueprint.route('/', methods=['GET'])(mainController.index)
web_blueprint.route('/predict', methods=['GET'])(mainController.prediction)
web_blueprint.route('/predict/result/<id>', methods=['GET'])(mainController.details)
web_blueprint.route('/predict/result/<id>/details', methods=['GET'])(mainController.detailSrap)