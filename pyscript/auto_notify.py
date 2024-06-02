from constants import (
  AUTO_NOTIFY_SENSORS_HOUSING, DEFAULT_NOTIFICATION_TARGET, 
  EXPR_TIME_WORKTIME, EXPR_TIME_UPDATE_SENSORS_HOUSING,
  AUTO_NOTIFY_SCRAPE_HOUSING_DELAY_RANDOM_MIN, AUTO_NOTIFY_SCRAPE_HOUSING_DELAY_RANDOM_MAX
  
)
from utils import expr

import random

sensors = AUTO_NOTIFY_SENSORS_HOUSING
default_notification_target = DEFAULT_NOTIFICATION_TARGET

# Automation
@state_trigger(expr([str(key) for key in sensors.keys()]))
def notify_housing(target=default_notification_target, default=True, var_name=None, value=None, old_value=None, **kwargs):
  if old_value not in STATES_HA_UNDEFINED:
    pyscript.notify(message=var_name, data={ "shortcut": {
          "name": SHORTCUT_HOUSING_NAME,
          "input": entities.get(var_name),
          "ignore_result": "ignore"
        } }, target=target )

# Helper

@time_active(EXPR_TIME_WORKTIME)
@time_trigger(EXPR_TIME_UPDATE_SENSORS_HOUSING)
def update_sensors_housing(sensors=sensors):
  task.sleep(random.randint(AUTO_NOTIFY_SCRAPE_HOUSING_DELAY_RANDOM_MIN, AUTO_NOTIFY_SCRAPE_HOUSING_DELAY_RANDOM_MAX))
  for sensor in sensors:
    homeassistant.update_entity(entity_id=sensor)