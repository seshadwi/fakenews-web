from flask import Blueprint
from controllers import mainController

blueprint = Blueprint('web', __name__)

blueprint.route('/', methods=['GET'])(mainController.index)