import os
import urllib
import webapp2

from globals import Jinja

class MainPage(webapp2.RequestHandler):
    def get(self):
        template = Jinja().get_template('index.html')
        template_values = {}
        self.response.write(template.render(template_values))
