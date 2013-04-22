from views.web import *
from views.socket import *
from settings import STATIC_PATH
from tornado.web import StaticFileHandler


urlpatterns = [
    (r"/", FrontPage),
    (r"/socket", ClientSocket),
    (r"/push", Pusher),
    (r"/auth", AuthToken),
    (r"/bans", BanManager),
    (r'/static/(.*)', StaticFileHandler, {'path': STATIC_PATH}),
]
