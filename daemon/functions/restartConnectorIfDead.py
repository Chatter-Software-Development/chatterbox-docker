import subprocess
import logging

def restartConnectorIfDead():
    try:
        connectorStatus = subprocess.check_output(["systemctl", "is-active", "chatterconnector"], universal_newlines=True).strip()
    except Exception as e:
        connectorStatus = 'inactive'
    if connectorStatus == 'active':
        print(f'[CONNECTOR] Chatter connector service is running')
        return
    elif connectorStatus == 'activating':
        print(f'[CONNECTOR] Chatter connector service is starting')
        logging.info(f'[CONNECTOR] Chatter connector service is starting')
        return
    
    try:
        logging.info(f'[CONNECTOR] Chatter connector service died, restarting')
        print(f'[CONNECTOR] Chatter connector service died, restarting')
        subprocess.run(["sudo", "systemctl", "restart", "chatterconnector.service"])
    except Exception as e:
        logging.error(f'[CONNECTOR] Failed to restart chatter connector service. {e}')
        print(f'[CONNECTOR] Failed to restart chatter connector service. {e}')