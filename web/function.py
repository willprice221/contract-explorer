import os
import urllib
import webapp2

from globals import Jinja

class FunctionPage(webapp2.RequestHandler):
    def get(self, contract_id, function_id):
        template = Jinja().get_template('function.html')
        template_values = {
            'contract': contract_id,
            'contract_id': contract_id,
            'function': function_id,
            'function_id': function_id
        }
        self.response.write(template.render(template_values))
