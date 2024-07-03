from constants.entities import AUTO_PRESENCE_ENTITIES
from constants.mappings import PERSISTENCE_ENTITY_AUTO_PRESENCE
from constants.settings import AUTO_PRESENCE_TRANSITION

from utils import *

trigger = []

def presence_factory(room, action):
  
  @time_trigger('startup')
  def presence_init(): 
    state.persist(PERSISTENCE_ENTITY_AUTO_PRESENCE)
    homeassistant.update_entity(entity_id=entity)

  @state_trigger([expr(entity, str(condition.get('condition'))) for entity, condition in AUTO_PRESENCE_ENTITIES.get(room).get('indicators').items()], state_hold=AUTO_PRESENCE_ENTITIES.get(room).get('indicators').get('duration'))
  @logged
  def presence(var_name=None):
    indicator_weight = weight(room, 'indicators')
    exclusion_weight = weight(room, 'exclusions')
    if action == 'on' and indicator_weight >= 1 and exclusion_weight == 0:
      persist(room, 'on')
      transition(room, 'on')
    elif action == 'off' and (indicator_weight < 1 or exclusion_weight > 0):
      persist(room, 'on')
      transition(room, 'off')
  trigger.append(presence)

def persist(room, action):
  state.set(PERSISTENCE_ENTITY_AUTO_PRESENCE, "'{}'".format(str(state.get(f"{entity}.wohnzimmer")) or str(state.get(f"{entity}.schlafzimmer"))), attributes={room: action})
  homeassistant.update_entity(entity_id=PERSISTENCE_ENTITY_AUTO_PRESENCE)
  state.persist(PERSISTENCE_ENTITY_AUTO_PRESENCE)

def weight(room, category):
  return 0 # sum([item.get('weight', 1) for item in AUTO_PRESENCE_ENTITIES[room][category].values()]) # TODO: if eval(item['condition'])])
  
def transition(room, action):
  for transition in AUTO_PRESENCE_TRANSITION.get(room, {}).get(action, []):
    if eval(transition['condition']):
      transition['action']()
      
# Initialization

for room in AUTO_PRESENCE_ENTITIES:
  presence_factory(room, 'on')
  presence_factory(room, 'off')