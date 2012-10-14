#item list generator
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from basetypes import *
import os,datetime,logging
    
class EditText(webapp.RequestHandler):
    def get(self):
        self.response.out.write('''
<!DOCTYPE html>
<html>
    <head>
        <title>%s</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    </head>
    <body>
        <form method="POST" action="/add/company">
            <textarea rows="20" cols="90" name="text"></textarea><br/>
            <input type="submit" value="Submit"/>
        </form>
    </body>
</html>
            ''' % ('Add New Company'))

    def post(self):
        rawdata = self.request.get('text').replace('\r\n','\n')
        for dataline in rawdata.split('\n'):
            logging.info(repr(dataline))
            compinfo = db.GqlQuery("SELECT * FROM Company WHERE Name='%s'"% dataline)
            result = compinfo.fetch(1)
        
            if len(result)==0 and dataline!='': 
                newcomp = Company()
                newcomp.Name = dataline
                newcomp.put()
            else:
                continue
        return

def main():
    application = webapp.WSGIApplication([(r'/.*', EditText)],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
