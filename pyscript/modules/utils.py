import importlib

from constants.config import CFG_LOG_LOGGER, CFG_LOG_LEVEL, CFG_LOGFILE_DEBUG_FUNCTION_STARTED, CFG_LOGFILE_IMPORT_RETRIES
from constants.mappings import MAP_STATE_HA_UNDEFINED
from exceptions import ForwardException

def expr(entity, expression="", comparator="==", defined=True, operator='or'):
  if entity and not isinstance(entity, str):
    if isinstance(entity, list):
      items = [f"({expr(item, expression, comparator, defined)})" for item in entity]
    if isinstance(entity, dict):
      items = [f"({expr(key, value, expression, comparator, defined)})" for key, value in entity.items()]
    return f" {operator} ".join(items) if items else None

  conditions = []
  if defined:
    conditions.append(f"{entity} is not None")
    states_undefined_str = ", ".join([f'\"{state}\"' for state in MAP_STATE_HA_UNDEFINED])
    conditions.append(f"{entity} not in [{states_undefined_str}]")
      
  if expression:
    if isinstance(expression, list):
      if comparator is None or comparator == "==" or comparator == "in":
        conditions.append(f"{entity} in {expression}")
      elif comparator == "!=":
        conditions.append(f"{entity} not in {expression}")
    if isinstance(expression, (int, float)) or comparator in ['<', '>']:
      conditions.append(f"float({entity}) {comparator} {expression}")
    elif isinstance(expression, str):
      conditions.append(f"{entity} {comparator} \'{expression}\'")
    # else:
      # conditions.append(f"{entity} {comparator} {expression}")
  else:
    conditions.append(f"{entity}")

  return " and ".join(conditions)

# Logging

def debug(msg="", title=""):
  if title: 
    msg = f"[{title}] {msg}"
  if msg:
    logfile = importlib.import_module("logfile")
    logfile.Logfile.debug(msg)

def log(msg="", title="", logger=CFG_LOG_LOGGER, level=CFG_LOG_LEVEL, **kwargs):
  if title: 
    msg = f"[{title}] {msg}"
  if msg: 
    system_log.write(message=str(msg), logger=logger, level=level)

# Monitoring 

def _monitored(func, log_func, debug_function_started=CFG_LOGFILE_DEBUG_FUNCTION_STARTED):
  def wrapper(*args, **kwargs):
    if kwargs.get('context'): del kwargs['context']
    context = ".".join([func.global_ctx_name, func.name]) if hasattr(func, 'global_ctx_name') and hasattr(func, 'name') else ""
    if debug_function_started:
      debug(f"{log_func_format(func, args, kwargs)}", title=context)
    try:
      result = func(*args, **kwargs)
    except Exception as e:
      raise ForwardException(e, context)
    finally:
      if result and log_func == "log":
        log(log_func_format(func, args, kwargs, result), title=context)
      debug(log_func_format(func, args, kwargs, result), title=context)
    return result
  return wrapper

def debugged(func):
  return _monitored(func, "debug")

def logged(func):
  return _monitored(func, "log")

# Utility

def logfile_init(name=None):
  for attempt in range(CFG_LOGFILE_IMPORT_RETRIES):
    try:
      logfile = importlib.import_module("logfile")
      if name:
        return logfile.Logfile(name)
      return logfile
    except ModuleNotFoundError:
      if attempt < CFG_LOGFILE_IMPORT_RETRIES - 1:
        task.sleep(1)
      else:
        raise
    except Exception as e:
      raise e

def logs(obj):
  if isinstance(obj, str):
    return obj
  elif isinstance(obj, dict):
    items = []
    for k in obj.keys():
      items.append(f"{k}={logs(obj.get(k, ''))}")
    return ", ".join(items)
  elif isinstance(obj, (list, tuple)):
    items = [logs(item) for item in obj]
    return f"[{', '.join(items)}]"
  else:
    try:
      attributes = vars(obj)
      attrs = []
      for key in attributes.keys():
        attrs.append(f"{key}={logs(attributes.get(key, ''))}")
      return f"{type(obj).name}({', '.join(attrs)})"
    except TypeError:
      return str(obj)

def log_func_format(func, args, kwargs, result=None):
  log_func_format_args = ", ".join([str(arg) if arg else "" for arg in args]) if args else None
  log_func_format_kwargs = ", ".join([f"{k}={v}" for k, v in kwargs.items() if k != "context"]) if kwargs else None
  log_func_format_arg = ", ".join([str(arg) if arg is not None else "" for arg in [log_func_format_args, log_func_format_kwargs] if arg])
  return f"{func.name if hasattr(func, 'name') else ''}" + f"({log_func_format_arg})" + (f": \n-> {result}" if result else "")