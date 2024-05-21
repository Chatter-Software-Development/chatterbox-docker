import requests
import subprocess
import logging
import socket

from const import API_BASE_URL, HOSTNAME

from .executeCommand import executeCommand

def sendHeartbeat(config):
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
        }
    })
    if response.status_code == 200:
        data = response.json()
        if 'commands' in data:
            for command in data['commands']:
                try:
                    executeCommand(command)
                except Exception as e:
                    logging.error(f'[COMMAND] Failed to execute command \'{command}\'. {e}')
                    print(f'[COMMAND] Failed to execute command \'{command}\'. {e}')
        return True
    else:
        logging.error(f'[HEARTBEAT] Failed to send heartbeat. HTTP {response.status_code} {response.reason}')
        print(f'[HEARTBEAT] Failed to send heartbeat. HTTP {response.status_code} {response.reason}')
        print(response.text)
        print(response.json())
        return False