from tornado.web import RequestHandler
from tornado.template import Loader
from settings import TEMPLATE_PATH

class WebRequestHandler(RequestHandler):
    def initialize(self):
        self.template_path = TEMPLATE_PATH
        #print TEMPLATE_PATH

    def render(self, template_name, params=None):
        loader = Loader(self.template_path)
        html = loader.load(template_name).generate(**params)
        self.write(html)
