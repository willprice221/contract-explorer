import os
import urllib
import webapp2

from globals import Jinja

class ContractPage(webapp2.RequestHandler):
    def get(self, contract_id):
        template = Jinja().get_template('contract.html')
        template_values = {
            'contract': contract_id,
            'contract_id': contract_id
        }
        self.response.write(template.render(template_values))
