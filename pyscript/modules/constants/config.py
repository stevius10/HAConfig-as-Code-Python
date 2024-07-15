from constants.secrets import SEC_SYSTEM_FILES

CFG_EVENT_STARTED_DELAY = 1

CFG_LOG_FILE_LOG = "home-assistant.log"
CFG_LOG_LOGGER = "py"
CFG_LOG_LEVEL = "info"
CFG_LOG_SIZE = 20
CFG_LOG_TAIL = 7

CFG_LOG_HISTORY_SIZE = 48
CFG_LOG_HISTORY_SUFFIX = "1"
CFG_LOG_ARCHIV_SIZE = 32768
CFG_LOG_ARCHIV_SUFFIX = "2"

CFG_LOG_SETTINGS_IO_RETRY = 4
CFG_LOG_SETTINGS_DELAY_BLOCK = 5

CFG_LOG_SETTINGS_ENVIRONMEMT_LENGTH = 12

CFG_LOGFILE_FORMAT = "%(asctime)s: %(message)s"
CFG_LOGFILE_LOG_SIZE = 10
CFG_LOGFILE_DEBUG_FILE = "messages"

CFG_LOGFILE_DEBUG_FUNCTION_STARTED = False
CFG_LOGFILE_IMPORT_RETRIES = 4

CFG_NOTIFICATION_TARGET_DEFAULT = "home"

CFG_PATH_DIR_CONFIG = "/config"
CFG_PATH_DIR_LOG = f"{CFG_PATH_DIR_CONFIG}/logs"
CFG_PATH_DIR_FILES = f"{CFG_PATH_DIR_CONFIG}/files"
CFG_PATH_DIR_STORAGE = f"{CFG_PATH_DIR_CONFIG}/.storage"

CFG_PATH_DIR_PY = f"{CFG_PATH_DIR_CONFIG}/pyscript"
CFG_PATH_DIR_PY_LOGS = f"{CFG_PATH_DIR_PY}/logs"
CFG_PATH_DIR_PY_LOGS_COMPONENTS = f"{CFG_PATH_DIR_LOG}/components"

CFG_PATH_DIR_PY_NATIVE = f"{CFG_PATH_DIR_CONFIG}/pyscript/python"

CFG_PATH_DIR_SUPERVISOR = "/homeassistant"
CFG_PATH_DIR_SUPERVISOR_LOGS = f"{CFG_PATH_DIR_SUPERVISOR}/logs"

CFG_PATH_FILE_LOG = f"{CFG_PATH_DIR_CONFIG}/{CFG_LOG_FILE_LOG}"
CFG_PATH_FILE_PY_LOG_SUPERVISOR = f"{CFG_PATH_DIR_SUPERVISOR}/{CFG_LOG_FILE_LOG}"

CFG_SERVICE_ENABLED_AIR_CONTROL = False
CFG_SERVICE_ENABLED_SYNC_GIT = True
CFG_SERVICE_ENABLED_SCRAPE_HOUSING = True

# System

CFG_SYSTEM_ENVIRONMENT = {
  "PYTHONDONTWRITEBYTECODE": "1",
  "ZDOTDIR": f"{CFG_PATH_DIR_STORAGE}/zsh"
}

CFG_SYSTEM_FILES = { **SEC_SYSTEM_FILES, 
  f"{CFG_PATH_DIR_FILES}/.zshrc": f"{CFG_SYSTEM_ENVIRONMENT['ZDOTDIR']}/.zshrc"
}

CFG_SYSTEM_LINKS = {
  CFG_PATH_DIR_SUPERVISOR_LOGS: CFG_PATH_DIR_PY_LOGS,
  CFG_PATH_FILE_PY_LOG_SUPERVISOR: f"{CFG_PATH_DIR_LOG}/{CFG_LOG_FILE_LOG}",
  f"{CFG_PATH_FILE_PY_LOG_SUPERVISOR}.{CFG_LOG_HISTORY_SUFFIX}": f"{CFG_PATH_DIR_LOG}/{CFG_LOG_FILE_LOG}.{CFG_LOG_HISTORY_SUFFIX}",
  f"{CFG_PATH_FILE_PY_LOG_SUPERVISOR}.{CFG_LOG_ARCHIV_SUFFIX}": f"{CFG_PATH_DIR_LOG}/{CFG_LOG_FILE_LOG}.{CFG_LOG_ARCHIV_SUFFIX}"
}