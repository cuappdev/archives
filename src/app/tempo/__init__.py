from flask import Blueprint
from app import *

# Tempo Blueprint
tempo = Blueprint('tempo', __name__, url_prefix = '')

# Import all models
from models._all import *

# Import all controllers
from controllers.user_authentication_controller import *

controllers = [
  UserAuthenticationController()
]

# Setup all controllers
for controller in controllers:
  tempo.add_url_rule(
    controller.get_path(),
    controller.get_name(),
    controller.response,
    methods = controller.get_methods()
  )
