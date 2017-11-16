from flask import Blueprint
from app import *

events = Blueprint('events', __name__, url_prefix='/api')

from app.events.models._all import * # pylint: disable=C0413

from app.events.controllers.authenticate_user_controller import * # pylint: disable=C0413
from app.events.controllers.create_app_controller import * # pylint: disable=C0413
from app.events.controllers.create_events_controller import * # pylint: disable=C0413
from app.events.controllers.create_event_type_controller import * # pylint: disable=C0413
from app.events.controllers.create_user_controller import * # pylint: disable=C0413
from app.events.controllers.get_apps_controller import * # pylint: disable=C0413
from app.events.controllers.get_events_controller import * # pylint: disable=C0413
from app.events.controllers.get_event_types_controller import * # pylint: disable=C0413
from app.events.controllers.update_session_controller import * # pylint: disable=C0413
from app.events.controllers.hello_world_controller import * # pylint: disable=C0413

controllers = [
    AuthenticateUserController(),
    CreateAppController(),
    CreateEventsController(),
    CreateEventTypeController(),
    CreateUserController(),
    GetAppsController(),
    GetEventsController(),
    GetEventTypesController(),
    UpdateSessionController(),
    HelloWorldController(),
]

for controller in controllers:
  print controller.get_methods(), controller.get_path(), controller.get_name()
  events.add_url_rule(
      controller.get_path(),
      controller.get_name(),
      controller.response,
      methods=controller.get_methods()
  )
