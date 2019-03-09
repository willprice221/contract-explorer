import os
import urllib
import webapp2

from google.appengine.api import urlfetch
import json
import logging

from globals import Jinja

class ContractPage(webapp2.RequestHandler):
    def post(self):
        address = self.request.get('address')
        self.redirect('/contract/%s' % address)

    def get(self, contract_address):
        # TODO: retrive from eveem BigTable to speed up
        contract_data = self.get_contract_data(contract_address)
        if contract_data is None:
            # todo: template w/ crying face
            return

        # TODO: we have functions. Run prediction and show topmost 5-10 w/ highest probability

        template = Jinja().get_template('contract.html')
        template_values = {
            'contract_address': contract_address,
            'functions': contract_data['functions']
        }
        self.response.write(template.render(template_values))

    def get_contract_data(self, contract_address):
        url = 'https://eveem.org/code/%s.json' % contract_address
        logging.info('Loading %s as contract data' % url)

        try:
            result = urlfetch.fetch(url)
            if result.status_code == 200:
                return json.loads(result.content)
            else:
                logging.warning('API returned status %d url %s' % (result.status_code, url))
                self.response.status_int = 404
                return None
        except urlfetch.Error:
            logging.exception('Caught exception fetching url %s' % url)
            self.response.status_int = 500
            return None
