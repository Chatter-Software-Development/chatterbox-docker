import os
import json

from const import CONFIG_FILE

def getLocalConfig():
    HOME_DIRECTORY = os.path.expanduser("~")
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    return config