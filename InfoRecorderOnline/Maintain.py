from basetypes import *
import os,logging,datetime
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class GamesList(webapp.RequestHandler):
    def get(self):
        gamelist = game.all()
        for gameitem in gamelist:
            for charaid in gameitem.Characters:
                chrquery = Query(Character)
                ch = chrquery.filter('cid =',charaid).get()
                if ch==None:
                    logging.error('non-exist cid : %d in game %s'%(charaid,gameitem.Name))
                else:
                    if str(gameitem.key()) not in ch.Games: 
                        ch.Games.append(str(gameitem.key()))
                        ch.put()
                    # 'no seiyuu' does not need a list
                    if ch.sid == 0:continue
                    # update seiyuu table
                    syquery = Query(Seiyuu)
                    sy = syquery.filter('sid =',ch.sid).get()
                    if sy==None:
                        logging.error('non-exist sid : %d in character %s (cid %d)'%(charaid,gameitem.Name,ch.cid))
                    else:
                        if str(gameitem.key()) not in sy.Games: 
                            sy.Games.append(str(gameitem.key()))
                            sy.put()
        # 'no seiyuu' should have an empty list
        syquery = Query(Seiyuu)
        sy = syquery.filter('sid =',0).get()
        sy.Games = []
        sy.put()
        logging.info(sy.Games)

        # setup seiyuu count
        slist = Seiyuu.all()
        for s in slist:
            if s.Games:
                s.GamesCount = len(s.Games)
            else:
                s.Games = []
                s.GamesCount = 0
            s.put()

class ClearSeiyuuList(webapp.RequestHandler):
    def get(self):
        slist = Seiyuu.all()
        for s in slist:
            s.Games = []
            s.GamesCount = 0
            s.put()
def main():
    application = webapp.WSGIApplication([
        (r'/maintain/clearslist*', ClearSeiyuuList),
        (r'/.*', GamesList)
        ],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
