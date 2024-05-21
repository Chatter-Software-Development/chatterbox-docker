import os
import requests
from requests_toolbelt import MultipartEncoder
import logging

from functions.getLocalConfig import getLocalConfig

from const import API_BASE_URL, LOG_DIRECTORY

from helpers.loggerHelper import LoggerHelper

def dumpLogs():
    print('Dumping logs!')
    config = getLocalConfig()
    daemonLogPath = os.path.join(LOG_DIRECTORY, 'chatterdaemon.log')
    connectorLogPath = os.path.join(LOG_DIRECTORY, 'chatterconnector.log')

    try:
        with open(daemonLogPath, 'rb') as f:
            daemonLog = f.read()
    except FileNotFoundError:
        daemonLog = b''

    try:
        with open(connectorLogPath, 'rb') as f:
            connectorLog = f.read()
    except FileNotFoundError:
        connectorLog = b''

    encodedData = MultipartEncoder(fields={
        'auth[id]': config['boxID'],
        'auth[key]': config['key'],
        'daemonLog': ('chatterdaemon.log', daemonLog, 'text/plain'),
        'connectorLog': ('chatterconnector.log', connectorLog, 'text/plain')
    })
    
    response = requests.post(f'{API_BASE_URL}/com/chatterbox/logs', data=encodedData, headers={'Content-Type': encodedData.content_type})
    if response.status_code == 200:
        print(response.text)
        if daemonLog != b'':
            LoggerHelper.deleteLogfile()
            LoggerHelper.disposeLogger()
            LoggerHelper.initLogger()
        if connectorLog != b'':
            os.remove(connectorLogPath)
        logging.info(f'[LOGS] Successfully dumped logs.')
    else:
        print(response.text)
        logging.error(f'[LOGS] Failed to dump logs. HTTP {response.status_code} {response.reason}')
