#item list generator
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext.db import BadKeyError
from basetypes import *
import os,datetime,logging
    
class StatGame(webapp.RequestHandler):
    def get(self):
        games = game.all()
        ryearlist = {}
        companylist = {}
        pyearlist = {}
        charalist = []
        for g in games:
            ryear = g.rDate.year
            pyear = g.pDate1.year
            comp = db.get(g.Company).Name
            if ryear not in ryearlist.keys():
                ryearlist[ryear] = 1
            else:
                ryearlist[ryear] += 1

            if pyear not in pyearlist.keys():
                pyearlist[pyear] = 1
            else:
                pyearlist[pyear] += 1

            if comp not in companylist.keys():
                companylist[comp] = 1
            else:
                companylist[comp] += 1

            charalist.append(len(g.Characters))

        # logging.info(games)
        template_values = {
            'title' : 'Games Statistics',
            'bar' : {
                'ryear' : {'caption' : 'Release Year', 'data' : ryearlist},
                'pyear' : {'caption' : 'Play Year', 'data' : pyearlist},
                'comp' : {'caption' : 'Company', 'data' : companylist}
                },
            'hist' : {
                'chara' : {'caption' : 'Character number distribution', 'data' : charalist}
                }
        }

        path = os.path.join(os.path.dirname(__file__), './/template//statistics.html')
        #----end------------------------------------------------------------------------------------------
        self.response.out.write(template.render(path,template_values))


def main():
    application = webapp.WSGIApplication([
        (r'/stat/game', StatGame),
        (r'/stat.*', StatGame)
        ],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
