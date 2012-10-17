from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext.db import BadKeyError
from google.appengine.ext.db import Query
from basetypes import *
import os,datetime,logging
    
class Info(webapp.RequestHandler):
    def get(self):
        key = self.request.get('key','0')
        ifhidden = self.request.get('hidden','0')
        
        if key=='0':return
        #Switch with Ajax
        #----begin----------------------------------------------------------------------------------------
        try:
            gameinfo = db.get(key)
        except BadKeyError:
            self.error(404)
            return
        #----end------------------------------------------------------------------------------------------
        
        #----generate parameter list----------------------------------------------------------------------
        Characters = []
        for c in gameinfo.Characters:
            cquery = Query(Character)
            chara = cquery.filter('cid =',c).get()
            if chara != None:
                Characters.append([chara,chara.getSeiyuuName()])

        template_values = {
            'game' : gameinfo,
            'Company' : db.get(gameinfo.Company).Name,
            'Characters' : Characters
        }
        path = os.path.join(os.path.dirname(__file__), './/template//info.html')
        #----end------------------------------------------------------------------------------------------
        self.response.out.write(template.render(path,template_values))


def main():
    application = webapp.WSGIApplication([(r'/.*', Info)],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
