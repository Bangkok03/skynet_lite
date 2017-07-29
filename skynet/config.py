import ConfigParser
import os.path

CONFIG_FILE ="skynet_lite.settings"

DEFAULT_CONFIG = {
    "server": "localhost",
    "port": "8086",
    "user": "root",
    "password": "root",
    "database": "skynet_lite"
}

def write_if_missing():
  if not os.path.isfile(CONFIG_FILE):
    write_default_config()

def write_default_config():
  cfg = ConfigParser.ConfigParser()

  for key in DEFAULT_CONFIG:
    cfg.set('DEFAULT',key,DEFAULT_CONFIG[key])

  with open(CONFIG_FILE, 'wb') as f:
    cfg.write(f)

def get_config(cfg_name="DEFAULT"):
  write_if_missing()
  cfg = {}
  
  config = ConfigParser.ConfigParser()
  config.read(CONFIG_FILE)

  for key in DEFAULT_CONFIG:
    cfg[key] = config.get(cfg_name, key)
  
  return cfg
