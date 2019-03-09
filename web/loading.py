from flask import abort

import logging
import requests

def load_contract_data(contract_address):
    url = 'https://eveem.org/code/%s.json' % contract_address
    logging.info('Loading %s as contract data' % url)

    result = requests.get(url)
    if result.status_code is not 200:
        logging.warning('API returned status %d url %s' % (result.status_code, url))
        abort(404)

    return result.json()

def find_function_in_contract(contract_data, function_hash):
    flist = [fn for fn in contract_data['functions'] if fn['hash'] == function_hash]
    if not flist:
        logging.warning('No function %s found in contract %s' % (function_hash, contract_address))
        abort(404)
    return flist[0]
