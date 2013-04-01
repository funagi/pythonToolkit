from basetypes import *
import os,logging,datetime,json
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

def datefromiso(isodate):
    y=int(isodate[:4])
    m=int(isodate[5:7])
    d=int(isodate[8:10])
    return datetime.date(y,m,d)

class Show(webapp.RequestHandler):
    def get(self):
        pass
        
def main():
    application = webapp.WSGIApplication([
        (r'.*', Show)
        ],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
