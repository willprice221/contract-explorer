import webapp2

from main import MainPage
from contract import ContractPage
from function import FunctionPage

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/contract/(\w+)', ContractPage),
    ('/contract/(\w+)/(\w+)', FunctionPage),
], debug=True)
