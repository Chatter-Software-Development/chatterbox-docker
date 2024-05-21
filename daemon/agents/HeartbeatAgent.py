import requests
import subprocess
import logging
import socket

from models.Command import Command

from const import API_BASE_URL, HOSTNAME

from functions.executeCommand import executeCommand

class HeartbeatAgent:
    def __init__(self):
        self.pendingCommands = []
        self.completedCommands = []

    def sendHeartbeat(self, config):
        print('Sending heartbeat')
        
        try:
            connectorStatus = subprocess.check_output(["systemctl", "is-active", "chatterconnector"], universal_newlines=True).strip()
        except Exception as e:
            connectorStatus = 'inactive'
        
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 5000))
            localIp = s.getsockname()[0]
        except Exception:
            localIp = '127.0.0.1'
        finally:
            s.close()

        response = requests.post(f'{API_BASE_URL}/com/chatterbox/heartbeat', json={
            'auth': {
                'id': config['boxID'],
                'key': config['key'],
            },
            'data': {
                'hostname': HOSTNAME,
                'ip': localIp,
                'version': config['version'],
                'status': connectorStatus,
            },
            'executedCommands': [c.id for c in self.completedCommands],
        })
        if response.status_code == 200:
            print('[HEARTBEAT] Heartbeat sent successfully.')
            self.completedCommands = []
            data = response.json()
            print(data)
            print('[HEARTBEAT] Recieved commands:')
            print(data['commands'])
            self.pendingCommands = [Command(**command) for command in data['commands']]
            self.runPendingCommands()
            return True
        else:
            logging.error(f'[HEARTBEAT] Failed to send heartbeat. HTTP {response.status_code} {response.reason}')
            print(f'[HEARTBEAT] Failed to send heartbeat. HTTP {response.status_code} {response.reason}')
            print(response.text)
            print(response.json())
            return False
        
    def runPendingCommands(self):
        for command in self.pendingCommands:
            try:
                executeCommand(command)
                self.completedCommands.append(command)
            except Exception as e:
                logging.error(f'[COMMAND] Failed to execute command \'{command}\'. {e}')
                print(f'[COMMAND] Failed to execute command \'{command}\'. {e}')
        self.pendingCommands = []