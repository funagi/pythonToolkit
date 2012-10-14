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
        <form method="POST" action="/add/character">
            <div>Name,sid,imagekey</div>
            <textarea rows="20" cols="90" name="text"></textarea><br>
            <input type="submit" value="Submit"/>
        </form>
    </body>
</html>
            ''' % ('Add New CHaracters'))

    def post(self):
        rawdata = self.request.get('text').replace('\r\n','\n')
        for dataline in rawdata.split('\n'):
            data = dataline.split(',')
            charainfo = db.GqlQuery("SELECT * FROM Character WHERE name='%s' AND sid=%s"% (data[0], data[1]))
            result = charainfo.fetch(1)
        
            if len(result)==0: 
                newchara = Character()
                newchara.Name = data[0]
                newchara.sid = int(data[1])
                dbquery = db.GqlQuery('SELECT * FROM Character ORDER BY cid DESC')
                if dbquery.fetch(1):
                    new_id = dbquery.fetch(1)[0].cid+1
                else:
                    new_id = 0
                newchara.cid = new_id
                newchara.image = data[2]
                newchara.put()
            else:
                continue
        return

def main():
    application = webapp.WSGIApplication([(r'/.*', EditText)],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
