#item list generator
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from basetypes import *
import os,datetime,logging,json
    
class Search(webapp.RequestHandler):
    def get(self):
        
        showhidden = self.request.get('hidden','0')
        dataid = self.request.get('id','0')
        if dataid != '0':
            dataname = self.request.get('name','')


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
        
        searchlist = []
        for game in gamelist:
            if dataid in game.Seiyuu:
                searchlist.append(game)

        #----generate parameter list----------------------------------------------------------------------
        template_values = {
            'gamelist' : searchlist,
            'name' : dataname
            }
        path = os.path.join(os.path.dirname(__file__), './/template//search.html')
        #----end------------------------------------------------------------------------------------------
        self.response.out.write(template.render(path,template_values))

class SearchGameBySeiyuu(webapp.RequestHandler):
    def get(self):
        dataid = self.request.get('snum','0')
        datalist = []
        if dataid == '0':
            pass
        else:
            syquery = Query(Seiyuu)
            sys = syquery.filter('snum =',int(dataid)).run()
            for sy in sys:
                for gstr in sy.Games:
                    g = db.get(gstr)
                    datalist.append({
                        'icon' : str(g.Icon.key()),
                        'name' : g.Name
                        })
        self.response.out.write(json.dumps(datalist))

def main():
    application = webapp.WSGIApplication([
        (r'/search/game.*', SearchGameBySeiyuu),
        (r'/.*', Search)
        ],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
