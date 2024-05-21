from socket import gethostname
import os

API_BASE_URL = 'https://apiv2.chatter.dev'
HOSTNAME = gethostname()
HOME_DIRECTORY = os.path.expanduser("~")
LOG_DIRECTORY = os.path.join(HOME_DIRECTORY, 'logs')
CONFIG_DIRECTORY = os.path.join(HOME_DIRECTORY, '.config/Chatter')
os.makedirs(LOG_DIRECTORY, exist_ok=True)
os.makedirs(CONFIG_DIRECTORY, exist_ok=True)

CONFIG_FILE = os.path.join(CONFIG_DIRECTORY, 'config.json')


FANUC_HANDSHAKE_ENDPOINT = 'https://apiv2.chatter.dev/com/legacy/fanuc/handshake'
FANUC_TRANSACTIONS_ENDPOINT = 'https://apiv2.chatter.dev/com/legacy/fanuc/transactions'