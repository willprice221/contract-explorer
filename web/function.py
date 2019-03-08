import os
import urllib
import webapp2

from globals import Jinja

class FunctionPage(webapp2.RequestHandler):
    def get(self, contract_address, function_hash):
        template = Jinja().get_template('function.html')
        template_values = {
            'contract': contract_address,
            'contract_address': contract_address,
            'function': function_hash,
            'function_hash': function_hash
        }
        self.response.write(template.render(template_values))
