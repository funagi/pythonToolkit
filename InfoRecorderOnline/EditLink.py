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
    
class EditText(webapp.RequestHandler):
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
<html>
    <head>
        <title>%s</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    </head>
    <body>
        <center>
            <form method="POST" action="/editlink">
                <textarea rows="20" cols="90" name="memo">%s</textarea><br/>
                <input type="hidden" value="%s" name="Id"/>
                <input type="submit" value="Submit"/>
            </form>
        </center>
    </body>
</html>
            ''' % (game.Name+' - Links',game.Memo,game.Id))

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

        game.Memo = db.Text(newdata)
        game.put()
        return

def main():
    application = webapp.WSGIApplication([(r'/.*', EditText)],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
