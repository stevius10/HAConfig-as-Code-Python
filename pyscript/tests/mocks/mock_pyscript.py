class MockPyscript:
  def __init__(self):
    self.global_vars = {}
    self.triggers = []
    self.services = {}
    self.states = {}
    self.timers = {}
    self.events = []

  def call_service(self, domain, service, **kwargs):
    if domain in self.services and service in self.services[domain]:
      return self.services[domain][service](**kwargs)
    else:
      raise ValueError(f"Service {domain}.{service} not found")

  def set_state(self, entity_id, state, **kwargs):
    self.states[entity_id] = {'state': state, 'attributes': kwargs}

  def get_state(self, entity_id, attribute=None):
    if entity_id not in self.states:
      return None
    if attribute is None:
      return self.states[entity_id]['state']
    return self.states[entity_id]['attributes'].get(attribute)

  def fire_event(self, event_type, **kwargs):
    self.events.append({'event_type': event_type, 'data': kwargs})

  @staticmethod
  def pyscript_executor(func):
    def decorator(func):
      def wrapper():
        return func()
      return wrapper
    return decorator

  @staticmethod
  def service(func):
    def decorator(func):
      def wrapper():
        return func()
      return wrapper
    return decorator

  @staticmethod
  def state_trigger(*args, **kwargs):
    def decorator(func):
      def wrapper(var_name=None, value=None, old_value=None, **kwargs):
        return func(var_name=var_name, value=value, old_value=old_value, **kwargs)
      return wrapper
    return decorator

  @staticmethod
  def time_trigger(*args, **kwargs):
    def decorator(func):
      def wrapper(trigger_type="time", **kwargs):
        return func(trigger_type=trigger_type, **kwargs)
      return wrapper
    return decorator

  @staticmethod
  def event_trigger(*args, **kwargs):
    def decorator(func):
      def wrapper(trigger_type="event", event_type=None, **kwargs):
        return func(trigger_type=trigger_type, event_type=event_type, **kwargs)
      return wrapper
    return decorator

  @staticmethod
  def state_active(*args, **kwargs):
    def decorator(func):
      def wrapper(var_name=None, value=None, old_value=None, **kwargs):
        return func(var_name=var_name, value=value, old_value=old_value, **kwargs)
      return wrapper
    return decorator

  @staticmethod
  def time_active(*args, **kwargs):
    def decorator(func):
      def wrapper(trigger_type="time", **kwargs):
        return func(trigger_type=trigger_type, **kwargs)
      return wrapper
    return decorator

  @staticmethod
  def event_active(*args, **kwargs):
    def decorator(func):
      def wrapper(trigger_type="event", event_type=None, **kwargs):
        return func(trigger_type=trigger_type, event_type=event_type, **kwargs)
      return wrapper
    return decorator

def pyscript_executor(func):
  def decorator(func):
    def wrapper():
      return func()
    return wrapper
  return decorator

def service(func):
  def decorator(func):
    def wrapper():
      return func()
    return wrapper
  return decorator

def state_trigger(*args, **kwargs):
  def decorator(func):
    def wrapper(var_name=None, value=None, old_value=None, **kwargs):
      return func(var_name=var_name, value=value, old_value=old_value, **kwargs)
    return wrapper
  return decorator

def time_trigger(*args, **kwargs):
  def decorator(func):
    def wrapper(trigger_type="time", **kwargs):
      return func(trigger_type=trigger_type, **kwargs)
    return wrapper
  return decorator

def event_trigger(*args, **kwargs):
  def decorator(func):
    def wrapper(trigger_type="event", event_type=None, **kwargs):
      return func(trigger_type=trigger_type, event_type=event_type, **kwargs)
    return wrapper
  return decorator

def state_active(*args, **kwargs):
  def decorator(func):
    def wrapper(var_name=None, value=None, old_value=None, **kwargs):
      return func(var_name=var_name, value=value, old_value=old_value, **kwargs)
    return wrapper
  return decorator

def time_active(*args, **kwargs):
  def decorator(func):
    def wrapper(trigger_type="time", **kwargs):
      return func(trigger_type=trigger_type, **kwargs)
    return wrapper
  return decorator

def event_active(*args, **kwargs):
  def decorator(func):
    def wrapper(trigger_type="event", event_type=None, **kwargs):
      return func(trigger_type=trigger_type, event_type=event_type, **kwargs)
    return wrapper
  return decorator