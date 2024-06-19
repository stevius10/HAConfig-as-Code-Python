from constants.config import *
from constants.devices import *
from constants.events import *
from constants.expressions import *
from constants.mappings import *
from constants.settings import *

from utils import *

import random

trigger = []

# Automation

# Housing

@event_trigger(EVENT_HOUSING_INITIALIZED)
def init_housing():
  @state_trigger(expr(entity=[name for name in state.names() if PERSISTANCE_SCRAPE_HOUSING_SENSOR_PREFIX in name]))
  def notify_housing(target=DEFAULT_NOTIFICATION_TARGET, default=True, var_name=None, value=None, old_value=None):
    if value not in STATES_UNDEFINED:
      pyscript.shortcut(message=f"{var_name}: {value}", shortcut=SHORTCUT_HOUSING_NAME, input=SERVICE_SCRAPE_HOUSING_PROVIDERS.get(var_name.split(".")[1].removeprefix(PERSISTANCE_SCRAPE_HOUSING_SENSOR_PREFIX)).get("url"))
  trigger.append(notify_housing)