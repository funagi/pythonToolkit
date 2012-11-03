#item list generator
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from basetypes import *
import os,datetime,logging
    
class AddCharacter(webapp.RequestHandler):
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
            <input type="submit" value="Submit"/><br/>
            <p>AMIfv95okg1m9KhvbYhXEHcqEhnOflFSj4paCzbWDq_qDwjvuK-_rYsgveF5ehqMp-rmxZfuYC47x4kXmkrfTcdfJ2u4O3aYAuNaHZoKi8QfhrSLN_xMsd7tjgtGxkdEQkp-JzZjqR0Cd5gMWesygGikVUEljJFCRQ</p>
        </form>
    </body>
</html>
            ''' % ('Add New Characters'))

    def post(self):
        rawdata = self.request.get('text').replace('\r\n','\n')
        # get latest id
        dbquery = db.GqlQuery('SELECT * FROM Character ORDER BY cid DESC')
        if dbquery.fetch(1):
            new_id = dbquery.fetch(1)[0].cid+1
        else:
            new_id = 1

        for dataline in rawdata.split('\n'):
            data = dataline.split(',')
            # charainfo = db.GqlQuery("SELECT * FROM Character WHERE name='%s' AND sid=%s"% (data[0], data[1]))
            # result = charainfo.fetch(1)
        
            # if len(result)==0: 
            newchara = Character()
            newchara.Name = data[0]
            newchara.sid = int(data[1])
            
            newchara.cid = new_id
            newchara.image = data[2]
            newchara.put()
            new_id += 1
            # else:
            #     continue
        self.redirect('/show/character')
        return

class AddCompany(webapp.RequestHandler):
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

class AddSeiyuu(webapp.RequestHandler):
    def get(self):
        self.response.out.write('''
<!DOCTYPE html>
<html>
    <head>
        <title>%s</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    </head>
    <body>
        <form method="POST" action="/add/seiyuu">
            <div>Name,snum,isMain</div>
            <textarea rows="20" cols="90" name="text"></textarea><br/>
            <input type="submit" value="Submit"/>
        </form>
    </body>
</html>
            ''' % ('Add New Seiyuus'))

    def post(self):
        rawdata = self.request.get('text').replace('\r\n','\n')
        # get latest id
        dbquery = db.GqlQuery('SELECT * FROM Seiyuu ORDER BY sid DESC')
        if dbquery.fetch(1):
            new_id = dbquery.fetch(1)[0].sid+1
        else:
            new_id = 1

        for dataline in rawdata.split('\n'):
            data = dataline.split(',')
            charainfo = db.GqlQuery("SELECT * FROM Seiyuu WHERE Name='%s' AND snum=%s"% (data[0], data[1]))
            result = charainfo.fetch(1)
        
            if len(result)==0: 
                newseiyuu = Seiyuu()
                newseiyuu.Name = data[0]
                newseiyuu.snum = int(data[1])
                if data[2]=="1":
                    newseiyuu.isMain = True
                else:
                    newseiyuu.isMain = False
                
                newseiyuu.sid = new_id
                newseiyuu.put()
                new_id += 1
            else:
                continue
        self.redirect('/show/seiyuu')
        return

def main():
    application = webapp.WSGIApplication([
        (r'/add/character', AddCharacter),
        (r'/add/seiyuu', AddSeiyuu),
        (r'/add/company', AddCompany),
        (r'.*', AddCharacter)
        ],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
