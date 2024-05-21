import os
import requests
import logging
import json
import subprocess
import time
import hashlib
import tempfile
import shutil

from const import API_BASE_URL, CONFIG_FILE

def updateCheck(config, force=False):
    print('Checking for updates...')
    if not force:
        logging.info('[UPDATE] Checking for updates...')
    else:
        logging.info('[UPDATE] Running forced update')
    response = requests.get(f'{API_BASE_URL}/com/version?type=CHATTERBOX')
    if response.status_code == 200:
        data = response.json()

        try:
            localVersion = config['version']
            remoteVersion = data['data']['version']
            remoteUrl = data['data']['url']
            hash = data['data']['hash']
        except KeyError:
            print('Failed to parse version data. Aborting update.')
            logging.error(f'[UPDATE CHECK] Failed to parse version data. Aborting update.')
            return

        if versionIsGreater(remoteVersion, localVersion) or force:
            if force:
                print(f'Forcing update to {remoteVersion} from {remoteUrl}')
                logging.info(f'[UPDATE CHECK] Forcing update to {remoteVersion} from {remoteUrl}')
            else:
                print(f'Update available. Updating {localVersion} to {remoteVersion} from {remoteUrl}')
                logging.info(f'[UPDATE CHECK] Update available. Updating {localVersion} to {remoteVersion} from {remoteUrl}')

            subprocess.run(["sudo", "systemctl", "stop", "chatterconnector.service"])
            timeout = 5
            start = time.time()
            while not checkServiceStatus('chatterconnector'):
                if time.time() - start > timeout:
                    print("Failed to stop ChatterConnector. Aborting update.")
                    logging.error(f'[UPDATE CHECK] Failed to stop ChatterConnector. Aborting update.')
                    return
                time.sleep(0.5)
            
            try:
                response = requests.get(remoteUrl)
                if response.status_code == 200:
                    exePath = os.path.join(os.path.expanduser('~'), 'chatterconnector/ChatterConnector')
                    if not os.path.exists(os.path.dirname(exePath)):
                        os.makedirs(os.path.dirname(exePath))

                    tempFilePath = os.path.join(tempfile.mkdtemp(), 'ChatterConnector')

                    with open(tempFilePath, 'wb') as f:
                        f.write(response.content)

                    if getFileHash(tempFilePath) != hash:
                        print(f'Hash mismatch. Aborting update.')
                        logging.error(f'[UPDATE CHECK] Hash mismatch. Aborting update.')
                        return
                    
                    shutil.move(tempFilePath, exePath)

                    os.chmod(exePath, 0o755)

                    config['version'] = remoteVersion
                    with open(CONFIG_FILE, 'w') as f:
                        json.dump(config, f, indent=4)
                    print(f'Update successful. Restarting ChatterConnector.')
                    logging.info(f'[UPDATE CHECK] Update successful. Restarting ChatterConnector.')
                    subprocess.run(["sudo", "systemctl", "restart", "chatterconnector.service"])
                else:
                    print(f'Fetching latest executable failed. HTTP {response.status_code} {response.reason}')
                    logging.error(f'[UPDATE CHECK] Fetching latest executable failed. HTTP {response.status_code} {response.reason}')
            except Exception as e:
                print(f'Fetching latest executable failed. {e}')
                logging.error(f'[UPDATE CHECK] Fetching latest executable failed. {e}')

            subprocess.run(["sudo", "systemctl", "start", "chatterconnector.service"])

        else:
            logging.info(f'[UPDATE CHECK] No updates available. Current version: {localVersion}')
    else:
        print(f'Failed to fetch latest version. HTTP {response.status_code} {response.reason}')
        logging.error(f'[UPDATE CHECK] Failed to fetch latest version. HTTP {response.status_code} {response.reason}')

def versionIsGreater(remoteVersion, localVersion):
    remoteVersion = str(remoteVersion)
    if remoteVersion[0] == 'V':
        remoteVersion = remoteVersion[1:]
    localVersion = str(localVersion)
    if localVersion[0] == 'V':
        localVersion = localVersion[1:]
    # Remove the 'V' and split the version into major and minor components
    localVersion = list(map(int, localVersion.split('.')))
    remoteVersion = list(map(int, remoteVersion.split('.')))

    # Compare versions
    return remoteVersion > localVersion


def getFileHash(filePath):
        sha256Hash = hashlib.sha256()
        with open(filePath, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256Hash.update(byte_block)
        return sha256Hash.hexdigest()

def checkServiceStatus(serviceName):
    try:
        output = subprocess.check_output(["systemctl", "is-active", serviceName], universal_newlines=True).strip()
        return output == 'inactive'
    except subprocess.CalledProcessError as e:
        if e.returncode == 3:
            return True
        else:
            raise e