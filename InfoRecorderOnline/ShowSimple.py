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
        if start!='0':
            charagql += ' OFFSET %d' % int(start)
        if count!='0':
            charagql += ' LIMIT %d' % int(count)
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
            'Data' : Characters
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
            seiyuu.append([sy.sid,sy.Name,str(sy.isMain)])

        logging.info(seiyuu)
        template_values = {
            'title' : 'Seiyuu',
            'Headers' : ['SID', 'Name', 'isMain'],
            'Data' : seiyuu
        }

        path = os.path.join(os.path.dirname(__file__), './/template//showtable.html')
        #----end------------------------------------------------------------------------------------------
        self.response.out.write(template.render(path,template_values))


def main():
    application = webapp.WSGIApplication([
        (r'/show/character', ShowCharacters),
        (r'/show/seiyuu', ShowSeiyuu)
        ],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
