import subprocess

def getConnectorState():
    try:
        connectorStatus = subprocess.check_output(["systemctl", "is-active", "chatterconnector"], universal_newlines=True).strip()
    except Exception as e:
        connectorStatus = 'inactive'
    return connectorStatus == 'active'