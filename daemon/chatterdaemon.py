import time
import schedule
import logging
import os
import subprocess

# Load local modules
from agents.HeartbeatAgent import HeartbeatAgent
from agents.FanucServiceController import FanucServiceController
from functions.updateCheck import updateCheck
from functions.getLocalConfig import getLocalConfig
from functions.dumpLogs import dumpLogs

# Load functions
from functions.restartConnectorIfDead import restartConnectorIfDead

# Load helpers
from helpers.loggerHelper import LoggerHelper

# Load constants
from const import CONFIG_FILE

# Set up logging
LoggerHelper.initLogger()
logging.info(f'[SYSTEM] Starting Chatter Daemon')

# Load local configuration
try:
    config = getLocalConfig()
except FileNotFoundError:
    logging.error(f'Local configuration file not found at \'{CONFIG_FILE}\'. Exiting.')
    print(f'Local configuration file not found at \'{CONFIG_FILE}\'. Exiting.')
    dumpLogs()
    exit(1)

def isDocker():
    return os.path.isfile('/.dockerenv')

def main():
    heartbeatAgent = HeartbeatAgent()
    heartbeatAgent.sendHeartbeat(config)
    schedule.every(30).seconds.do(heartbeatAgent.sendHeartbeat, config)

    if not isDocker():
        fanucServiceController = FanucServiceController(config)
        fanucServiceController.configure()

        updateCheck(config)
        dumpLogs()

        schedule.every(30).seconds.do(restartConnectorIfDead)
        schedule.every().day.at("07:00").do(updateCheck, config)
        schedule.every().day.at("06:50").do(dumpLogs)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
