#item list generator
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext.db import BadKeyError
from basetypes import *
import os,datetime,logging
    
class ShowCharacters(webapp.RequestHandler):
    def get(self):
        start = self.request.get('start','0')
        count = self.request.get('count','0')
        charagql = 'SELECT __key__ FROM Character ORDER BY cid ASC'
        if count!='0':
            charagql += ' LIMIT %d,%d' % (int(start),int(count))
        logging.info(charagql)
        charaquery = db.GqlQuery(charagql)
        Characters = []
        for item in charaquery:
            chara = db.get(item)
            Characters.append([
                chara.cid,
                chara.Name,
                chara.getSeiyuuName(),
                chara.sid,
                '<a href="/data?key=%s">link</a>'%chara.image.key()
                ])

        template_values = {
            'title' : 'Characters',
            'Headers' : ['CID', 'Name', 'Seiyuu', 'SID', 'Image'],
            'Data' : Characters,
            'links' : [
            {'link':'/add/character','name':'Add new characters'},
            {'link':'/add/seiyuu','name':'Add new seiyuu'},
            {'link':'/add/company','name':'Add new company'},
            {'link':'/upload?type=simple','name':'Simple upload'}
            ]
        }

        path = os.path.join(os.path.dirname(__file__), './/template//showtable.html')
        #----end------------------------------------------------------------------------------------------
        self.response.out.write(template.render(path,template_values))


class ShowSeiyuu(webapp.RequestHandler):
    def get(self):
        start = self.request.get('start','0')
        count = self.request.get('count','0')
        seiyuugql = 'SELECT __key__ FROM Seiyuu ORDER BY sid ASC'
        if start!='0':
            seiyuugql += ' OFFSET %d' % int(start)
        if count!='0':
            seiyuugql += ' LIMIT %d' % int(count)
        logging.info(seiyuugql)
        charaquery = db.GqlQuery(seiyuugql)
        seiyuu = []
        for item in charaquery:
            sy = db.get(item)
            seiyuu.append([
                sy.sid,
                sy.Name,
                str(sy.isMain),
                '<a href="http://beautyplanets.web.fc2.com/VADB/actor/c_%04d.html">%d</a>'%(sy.snum,sy.snum)
                ])

        # logging.info(seiyuu)
        template_values = {
            'title' : 'Seiyuu',
            'Headers' : ['SID', 'Name', 'isMain', 'VADB Link'],
            'Data' : seiyuu,
            'links' : [
            {'link':'/add/character','name':'Add new characters'},
            {'link':'/add/seiyuu','name':'Add new seiyuu'},
            {'link':'/add/company','name':'Add new company'},
            {'link':'/upload?type=simple','name':'Simple upload'}
            ]
        }

        path = os.path.join(os.path.dirname(__file__), './/template//showtable.html')
        #----end------------------------------------------------------------------------------------------
        self.response.out.write(template.render(path,template_values))

class ShowGame(webapp.RequestHandler):
    def get(self):
        start = self.request.get('start','0')
        count = self.request.get('count','0')
        gamegql = 'SELECT __key__ FROM game ORDER BY rDate ASC'
        if start!='0':
            gamegql += ' OFFSET %d' % int(start)
        if count!='0':
            gamegql += ' LIMIT %d' % int(count)
        logging.info(gamegql)
        gamequery = db.GqlQuery(gamegql)
        games = []
        for item in gamequery:
            gm = db.get(item)
            games.append([
                gm.Name,
                db.get(gm.Company).Name,
                gm.rDate.strftime('%Y-%m-%d'),
                gm.pDate1.strftime('%Y-%m-%d'),
                gm.pDate2.strftime('%Y-%m-%d'),
                '<a href="/edit?key=%s">Edit</a>'%item
                ])

        # logging.info(games)
        template_values = {
            'title' : 'Games',
            'Headers' : ['Name', 'Company', 'Release', 'Start', 'Finish', 'Edit'],
            'Data' : games,
            'links' : [
            {'link':'/add/character','name':'Add new characters'},
            {'link':'/add/seiyuu','name':'Add new seiyuu'},
            {'link':'/add/company','name':'Add new company'},
            {'link':'/upload','name':'Add new game'},
            {'link':'/upload?type=simple','name':'Simple upload'}
            ]
        }

        path = os.path.join(os.path.dirname(__file__), './/template//showtable.html')
        #----end------------------------------------------------------------------------------------------
        self.response.out.write(template.render(path,template_values))


def main():
    application = webapp.WSGIApplication([
        (r'/show/character', ShowCharacters),
        (r'/show/seiyuu', ShowSeiyuu),
        (r'/show/game', ShowGame),
        (r'/show.*', ShowGame)
        ],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
