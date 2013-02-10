# Add to path
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# Bootstrap the app
import tornado.ioloop
import tornado.web
import tornado.autoreload
import datetime
from urls import urlpatterns


# Server Auto Reload Hook

def auto_reload_hook():
    print "Server is starting: " + str(datetime.datetime.now())


application = tornado.web.Application(urlpatterns)
if __name__ == "__main__":
    application.listen(8888)
    tornado.autoreload.add_reload_hook(auto_reload_hook)
    tornado.autoreload.start()
    print "Server is starting: " + str(datetime.datetime.now())
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print ""
        print "Quitting"
        sys.exit(0)