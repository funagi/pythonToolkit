from basetypes import *
import logging,datetime
from google.appengine.ext import db,blobstore
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import images
from google.appengine.ext.webapp import blobstore_handlers

def datefromiso(isodate):
    y=int(isodate[:4])
    m=int(isodate[5:7])
    d=int(isodate[8:10])
    return datetime.date(y,m,d)

def getLastId():
    dbquery = db.GqlQuery('SELECT * FROM game ORDER BY Id DESC')
    max_id = dbquery.fetch(1)[0].Id
    return max_id+1

class UploadBinary(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        icon = self.get_uploads('Icon')[0]
        poster = self.get_uploads('Poster')[0]
        attachment = self.get_uploads('Attachment')[0]
        
        #get all the infomation
        args = self.request.arguments()
        data = {}
        
        for arg in args:
            data[arg] = self.request.get(arg)
            
        #generate and put game object
        game_temp = game()
        #parse id
        if ('Id' in data.keys()) and data['Id']=='':
            game_temp.Id = getLastId()
        else:
            game_temp.Id = int(data['Id'])
        #parse strings
        game_temp.Name = data['Name'].decode('utf-8')
        logging.info(repr(data['Name']))
        game_temp.Company = data['Company'].decode('utf-8')
        game_temp.Seiyuu = db.Text(data['Seiyuu'])
        game_temp.Memo = db.Text(data['Seiyuu'])
        #parse dates
        game_temp.rDate = datefromiso(data['rDate'])
        game_temp.pDate1 = datefromiso(data['pDate1'])
        game_temp.pDate2 = datefromiso(data['pDate2'])
        #parse binaries blobstore
        game_temp.Icon = icon
        game_temp.Poster = poster
        game_temp.Attachment = attachment
        #parse booleans
        if 'Hidden' in data.keys():
            game_temp.Hidden = True
        else:
            game_temp.Hidden = False
        game_temp.put()

def main():
    application = webapp.WSGIApplication([('/.*', UploadBinary)],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
