#item list generator
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext.db import BadKeyError
from basetypes import *
import os,datetime,logging
    
class EditCharacter(webapp.RequestHandler):
    def get(self):
        key = self.request.get('key','0')
        
        if key=='0':return
        #Switch with Ajax
        #----begin----------------------------------------------------------------------------------------
        try:
            gameinfo = db.get(key)
        except BadKeyError:
            self.error(500)
            return
        #----end------------------------------------------------------------------------------------------
        self.response.out.write('''
<html>
    <head>
        <title>%s</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    </head>
    <body>
        <form method="POST" action="/edit/character">
            <textarea rows="20" cols="90" name="Characters">%s</textarea>
            <input type="hidden" value="%s" name="key"/>
            <input type="submit" value="Submit"/>
        </form>
    </body>
</html>
            ''' % (gameinfo.Name+' - Characters',','.join([str(x) for x in gameinfo.Characters]),gameinfo.key()))

    def post(self):
        key = self.request.get('key','0')
        
        if key=='0':return
        #Switch with Ajax
        #----begin----------------------------------------------------------------------------------------
        try:
            gameinfo = db.get(key)
        except BadKeyError:
            self.error(500)
            return
        #----end------------------------------------------------------------------------------------------
        newdata = self.request.get('Characters')

        gameinfo.Characters = [int(x) for x in newdata.split(',')]
        gameinfo.put()
        return

class EditLink(webapp.RequestHandler):
    def get(self):
        Id = self.request.get('Id','0')
        
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
        game = result[0]
        self.response.out.write('''
<!DOCTYPE html>
<html>
    <head>
        <title>ExtLinks for %s</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    </head>
    <body>
        <center>
            <form method="POST" action="/edit/link">
                <textarea rows="20" cols="90" name="memo">%s</textarea><br/>
                <input type="hidden" value="%s" name="Id"/>
                <input type="submit" value="Submit"/>
            </form>
        </center>
    </body>
</html>
            ''' % (game.Name+' - Links',game.ExtLinks,game.Id))

    def post(self):
        Id = self.request.get('Id','0')
        
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
        game = result[0]

        newdata = self.request.get('memo')

        game.ExtLinks = db.Text(newdata)
        game.put()
        return

def main():
    application = webapp.WSGIApplication([
        (r'/edit/character', EditCharacter),
        (r'/edit/link', EditLink)
        ],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
