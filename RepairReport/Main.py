#item list generator
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from basetypes import *
import os,datetime,logging
    
class List(webapp.RequestHandler):
    def get(self):
        pass


def main():
    application = webapp.WSGIApplication([(r'/.*', List)],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
