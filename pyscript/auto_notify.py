from config import *
from utils import *

from homeassistant.const import EVENT_CALL_SERVICE

import random

entities = { 
  "sensor.v_friedrichsheim": { "url": "https://www.friedrichsheim-eg.de/category/freie-wohnungen/" }, 
  # "sensor.v_bmv": { "url": "https://www.bwv-berlin.de/wohnungsangebote.html" }, 
  "sensor.v_neukolln": { "url": "https://www.gwneukoelln.de/wohnungen/wohnungsangebote/" }, 
  "sensor.v_wbm": { "url": "https://www.wbm.de/wohnungen-berlin/angebote-wbm/" }, 
  "sensor.v_gewobag": { "url": "https://www.wbm.de/wohnungen-berlin/angebote-wbm/" }, 
  "sensor.v_inberlinwohnen": { "url": "https://www.gewobag.de/fuer-mieter-und-mietinteressenten/mietangebote/?bezirke%5B%5D=charlottenburg-wilmersdorf-charlottenburg&bezirke%5B%5D=friedrichshain-kreuzberg&bezirke%5B%5D=friedrichshain-kreuzberg-friedrichshain&bezirke%5B%5D=friedrichshain-kreuzberg-kreuzberg&bezirke%5B%5D=mitte&bezirke%5B%5D=mitte-gesundbrunnen&bezirke%5B%5D=mitte-wedding&bezirke%5B%5D=neukoelln&bezirke%5B%5D=neukoelln-buckow&bezirke%5B%5D=neukoelln-rudow&bezirke%5B%5D=pankow-prenzlauer-berg&bezirke%5B%5D=tempelhof-schoeneberg-schoeneberg&nutzungsarten%5B%5D=wohnung&gesamtmiete_von=&gesamtmiete_bis=700&gesamtflaeche_von=50&gesamtflaeche_bis=&zimmer_von=2&zimmer_bis=&sort-by=recent" }
}

notification_id_change_detection = "changedetection"

@state_trigger(expr([str(key) for key in list(entities.keys())]))
def notify_immo(**kwargs):
  if(kwargs.get("old_value") not in STATES_HA_UNDEFINED):
    notify.mobile_app_iphone(
      message="", #kwargs.get("var_name"), 
      data={
        "shortcut": {
          "name": "Notification-Monitor",
          "input": entities[kwargs.get("var_name")],
          "ignore_result": "ignore"
        }
      }
    )

@time_active(EXPR_TIME_ACTIVE)
@time_trigger(EXPR_TIME_UPDATE_SENSORS)
def update_sensors(): 
  task.sleep(random.randint(10, 600))
  for entity in entities:
    homeassistant.update_entity(entity_id=entity)

@event_trigger(EVENT_CALL_SERVICE, "domain == 'persistent_notification' and service == 'create'")
@log_context
def notify_persistent_notification(ns=None, ctx=None, **kwargs):
  service_data=kwargs.get("service_data")
  if service_data.get("notification_id") == notification_id_change_detection:
    notification_data = dict(actions=[dict(action="URI", title=service_data.get("message"), uri=service_data.get("title"))])
    notify.mobile_app_iphone(message=kwargs.get("service_data").get("message"), data=notification_data)
    persistent_notification.dismiss(notification_id=service_data.get("notification_id"))
    log(f"change detected", ns, ctx, service_data.get("title"))