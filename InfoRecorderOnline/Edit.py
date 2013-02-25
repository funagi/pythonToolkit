#item list generator
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext.db import BadKeyError
from basetypes import *
import os,datetime,logging

def datefromiso(isodate):
    y=int(isodate[:4])
    m=int(isodate[5:7])
    d=int(isodate[8:10])
    return datetime.date(y,m,d)
    
class EditCharacter(webapp.RequestHandler):
    def get(self):
        key = self.request.get('key','0')
        
        if key=='0':return
        #Switch with Ajax
        #----begin----------------------------------------------------------------------------------------
        try:
            gameinfo = db.get(key)
        except BadKeyError:
            logging.error('BadKeyError : %s'%key)
            self.response.out.write('Item with specific key does not exist!')
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
        self.redirect('/info?key=%s'%key)
        return

class EditCharacterDetail(webapp.RequestHandler):
    def get(self):
        key = self.request.get('key','0')
        
        if key=='0':return
        #Switch with Ajax
        #----begin----------------------------------------------------------------------------------------
        try:
            chara = db.get(key)
        except BadKeyError:
            logging.error('BadKeyError : %s'%key)
            self.response.out.write('Item with specific key does not exist!')
            return
        #----end------------------------------------------------------------------------------------------
        self.response.out.write('''
<html>
    <head>
        <title>%s</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    </head>
    <body>
        <form method="POST" action="/edit/charadetail">
            <table>
                <tr>
                    <td>CID</td>
                    <td>%d</td>
                </tr>
                <tr>
                    <td>Name</td>
                    <td><input type="text" name="Name" value="%s"/></td>
                </tr>
                <tr>
                    <td>Romaji</td>
                    <td><input type="text" name="Romaji" value="%s"/></td>
                </tr>
                <tr>
                    <td>SID</td>
                    <td><input type="text" name="sid" value="%s"/></td>
                </tr>
                <tr>
                    <td>Image</td>
                    <td><img src="/data?key=%s" width=50 height=50/></td>
                </tr>
            </table>
            <input type="hidden" value="%s" name="key"/>
            <input type="submit" value="Submit"/>
        </form>
    </body>
</html>
            ''' % ('Character Detail',
                chara.cid,
                chara.Name,
                chara.Romaji,
                chara.sid,
                chara.image.key(),
                chara.key()
                ))

    def post(self):
        key = self.request.get('key','0')
        
        if key=='0':return
        #Switch with Ajax
        #----begin----------------------------------------------------------------------------------------
        try:
            chara = db.get(key)
        except BadKeyError:
            self.error(500)
            return
        #----end------------------------------------------------------------------------------------------
        chara.Name = self.request.get('Name')
        chara.Romaji = self.request.get('Romaji')
        chara.sid = int(self.request.get('sid'))
        chara.put()

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
        key = self.request.get('key','0')
        
        if key=='0':return
        #Switch with Ajax
        #----begin----------------------------------------------------------------------------------------
        gameinfo = db.GqlQuery('SELECT * FROM game WHERE key=%s'%key)
        
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
        self.redirect('/info?key=%s'%key)
        return

class EditGame(webapp.RequestHandler):
    def get(self):
        key = self.request.get('key','0')
        
        if key=='0':return
        #Switch with Ajax
        #----begin----------------------------------------------------------------------------------------
        try:
            gameinfo = db.get(key)
        except BadKeyError:
            logging.error('BadKeyError : %s'%key)
            self.response.out.write('Item with specific key does not exist!')
            return
        #----end------------------------------------------------------------------------------------------
        # gather company info
        company2 = Company.all()
        company = []
        for com in company2:
            company.append({"key":com.key(),"Name":com.Name})

        template_values = {
            'game' : gameinfo,
            'company' : company
            }
        path = os.path.join(os.path.dirname(__file__), './template/EditGame.html')
        self.response.out.write(template.render(path,template_values))

    def post(self):
        key = self.request.get('key','0')
        
        if key=='0':return
        #Switch with Ajax
        #----begin----------------------------------------------------------------------------------------
        try:
            game_temp = db.get(key)
            logging.error('Key : %s'%key)
        except BadKeyError:
            logging.error('BadKeyError : %s'%key)
            self.error(500)
            return
        #----end------------------------------------------------------------------------------------------
        # get all the infomation
        args = self.request.arguments()
        data = {}
        for arg in args:
            data[arg] = self.request.get(arg)
        
        game_temp.Name = data['Name']
        logging.info(repr(data['Name']))
        game_temp.Company = data['Company']
        game_temp.ExtLinks = db.Text(data['ExtLinks'])
        game_temp.VADB = int(data['VADB'])
        game_temp.VNDB = int(data['VNDB'])
        game_temp.EGS = int(data['EGS'])
        #parse dates
        game_temp.rDate = datefromiso(data['rDate'])
        game_temp.pDate1 = datefromiso(data['pDate1'])
        game_temp.pDate2 = datefromiso(data['pDate2'])
        #parse binaries blobstore
        game_temp.Icon = data['Icon']
        game_temp.Poster = data['Poster']
        game_temp.Attachment = data['Attachment']

        if 'Hidden' in data.keys():
            game_temp.Hidden = True
        else:
            game_temp.Hidden = False
        game_temp.put()
        self.redirect('/main')

def main():
    application = webapp.WSGIApplication([
        (r'/edit/character', EditCharacter),
        (r'/edit/charadetail', EditCharacterDetail),
        (r'/edit/link', EditLink),
        (r'/edit/game', EditGame),
        (r'/edit.*', EditGame)
        ],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
