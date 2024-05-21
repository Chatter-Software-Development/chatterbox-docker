import subprocess
import threading
import logging

from .dumpLogs import dumpLogs

from functions.getLocalConfig import getLocalConfig
from functions.updateCheck import updateCheck

def executeCommand(command):
    logging.info(f'[COMMAND] Recieved command \'{command.id}: {command.command}\'.')
    if command.command.lower() == 'connector_restart':
        subprocess.run(["sudo", "systemctl", "restart", "chatterconnector.service"])
    elif command.command.lower() == 'daemon_restart':
        subprocess.run(["sudo", "systemctl", "restart", "chatterdaemon.service"])
    elif command.command.lower() == 'system_restart':
        subprocess.run(["sudo", "shutdown", "-r", "now"])
    elif command.command.lower() == 'dump_logs':
        threading.Thread(target=dumpLogs).start()
    elif command.command.lower() == 'force_update':
        threading.Thread(target=updateCheck, args=(getLocalConfig(), True)).start()
    else:
        raise Exception(f'Unknown command \'{command}\'.')