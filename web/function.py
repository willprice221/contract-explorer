import os
import urllib
import webapp2

from globals import Jinja

class FunctionPage(webapp2.RequestHandler):
    def get(self, contract_address, function_hash):
        # TODO: based on contract address and function hash, predict what are most similar to it.
        # TODO: provide the function name (i.e. read it from BigTable?)

        template = Jinja().get_template('function.html')
        template_values = {
            'contract': contract_address,
            'contract_address': contract_address,
            'function': function_hash,
            'function_hash': function_hash
        }
        self.response.write(template.render(template_values))
