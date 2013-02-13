from views.web import *
from views.socket import *


urlpatterns = [
    (r"/", FrontPage),
    (r"/socket", ClientSocket),
    (r"/push", Pusher),
    (r"/auth", AuthToken),
]