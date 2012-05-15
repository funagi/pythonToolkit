#item list generator
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from basetypes import *
import os,datetime,logging
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from google.appengine.dist import use_library
use_library('django', '0.96')
    
class List(webapp.RequestHandler):
    def get(self):
        
        showhidden = self.request.get('hidden','0')
        if showhidden == '1':
            showhidden = True
        else:
            showhidden = False
        #----begin----------------------------------------------------------------------------------------
        if showhidden:
            gamelist = db.GqlQuery('SELECT * FROM game ORDER BY Name ASC')
        else:
            gamelist = db.GqlQuery('SELECT * FROM game WHERE Hidden = FALSE ORDER BY Name ASC')
        if gamelist.count()==0: self.error(404)
        #----end------------------------------------------------------------------------------------------
        
        #----generate parameter list----------------------------------------------------------------------
        template_values = {
            'gamelist' : gamelist,
            }
        path = os.path.join(os.path.dirname(__file__), './/template//frame.html')
        #----end------------------------------------------------------------------------------------------
        self.response.out.write(template.render(path,template_values))


def main():
    application = webapp.WSGIApplication([(r'/.*', List)],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
