import subprocess
import requests
import os
import json
import time
import logging

from const import API_BASE_URL, FANUC_HANDSHAKE_ENDPOINT, FANUC_TRANSACTIONS_ENDPOINT

class FanucServiceController:
    def __init__(self, config):
        self.config = config
        return
    
    def configure(self):
        if not self._getRemoteActivationState():
            if self._getStatus():
                logging.info('[FANUC SERVICE] Disabling Fanuc service...')
                print('[FANUC SERVICE] Disabling Fanuc service...')
                self.disable()
            return
        
        logging.info('[FANUC SERVICE] Configuring Fanuc service...')
        print('[FANUC SERVICE] Configuring Fanuc service...')

        # Write the config file
        serviceConfigLocation = os.path.join(os.path.expanduser('~'), 'fanuc/appSettings.json')
        serviceConfig = {
            'boxID': self.config['boxID'],
            'key': self.config['key'],
            'handshakeEndpoint': FANUC_HANDSHAKE_ENDPOINT,
            'endpoint': FANUC_TRANSACTIONS_ENDPOINT
        }

        with open(serviceConfigLocation, 'w') as f:
            f.write(json.dumps(serviceConfig))

        # Restart the service
        if not self._getStatus():
            logging.info('[FANUC SERVICE] Enabling Fanuc service...')
            print('[FANUC SERVICE] Enabling Fanuc service...')
            self.enable()
            self.restart()
        else:
            logging.info('[FANUC SERVICE] Fanuc service already enabled.')
            print('[FANUC SERVICE] Fanuc service already enabled.')
            

    
    def _getRemoteActivationState(self):
        response = requests.post(f'{API_BASE_URL}/com/handshake', json={
            'id': self.config['boxID'],
            'key': self.config['key']
        })
        data = response.json()
        return any([x['type'] == 1 for x in data['machines']])
    
    def ensureRunning(self):
        if not self._getStatus():
            self.start()
    
    def start(self):
        subprocess.run(["sudo", "systemctl", "start", "fanuc.service"])

    def stop(self):
        subprocess.run(["sudo", "systemctl", "stop", "fanuc.service"])

    def restart(self):
        subprocess.run(["sudo", "systemctl", "restart", "fanuc.service"])

    def enable(self):
        subprocess.run(["sudo", "systemctl", "enable", "fanuc.service"])

    def disable(self):
        self.stop()
        timeout = 2
        start = time.time()
        while self._getStatus():
            if time.time() - start > timeout:
                break
            time.sleep(.5)
        subprocess.run(["sudo", "systemctl", "disable", "fanuc.service"])
    
    def _getStatus(self):
        try:
            connectorStatus = subprocess.check_output(["systemctl", "is-active", "fanuc.service"], universal_newlines=True).strip()
        except Exception as e:
            connectorStatus = 'inactive'
        
        return connectorStatus == 'active'
