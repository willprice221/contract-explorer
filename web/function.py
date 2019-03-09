import os
import urllib
import webapp2

from google.appengine.api import urlfetch
import json
import logging

from globals import Jinja

class FunctionPage(webapp2.RequestHandler):
    def get(self, contract_address, function_hash):
        # TODO: based on contract address and function hash, predict what are most similar to it.
        function = self.get_function_data(contract_address, function_hash)
        if function is None:
            return

        template = Jinja().get_template('function.html')
        template_values = {
            'contract_address': contract_address,
            'function_hash': function_hash,
            'function': function
        }
        self.response.write(template.render(template_values))

    def get_function_data(self, contract_address, function_hash):
        url = 'https://eveem.org/code/%s.json' % contract_address
        logging.info('Loading %s as contract data' % url)

        try:
            result = urlfetch.fetch(url)
            if result.status_code == 200:
                contract_data = json.loads(result.content)
                flist = [fn for fn in contract_data['functions'] if fn['hash'] == function_hash]
                if not flist:
                    logging.warning('No function %s found in contract %s' % (function_hash, contract_address))
                    self.response.status_int = 404
                    return None
                return flist[0]
            else:
                logging.warning('API returned status %d url %s' % (result.status_code, url))
                self.response.status_int = 404
                return None
        except urlfetch.Error:
            logging.exception('Caught exception fetching url %s' % url)
            self.response.status_int = 500
            return None
