from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from basetypes import *
import os,datetime,logging
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from google.appengine.dist import use_library
use_library('django', '0.96')
    
class Info(webapp.RequestHandler):
    def get(self):
        Id = self.request.get('Id','0')
        ifhidden = self.request.get('hidden','0')
        
        if Id=='0':return
        #Switch with Ajax
        #----begin----------------------------------------------------------------------------------------
        gameinfo = db.GqlQuery('SELECT * FROM game WHERE Id=%s'%Id)
        
        result = gameinfo.fetch(1)
        logging.info(str(result))
        if len(result)==0: 
            self.error(404)
            return
        #----end------------------------------------------------------------------------------------------
        
        #----generate parameter list----------------------------------------------------------------------
        template_values = {'game' : result[0],}
        path = os.path.join(os.path.dirname(__file__), './/template//info.html')
        #----end------------------------------------------------------------------------------------------
        self.response.out.write(template.render(path,template_values))


def main():
    application = webapp.WSGIApplication([(r'/.*', Info)],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
