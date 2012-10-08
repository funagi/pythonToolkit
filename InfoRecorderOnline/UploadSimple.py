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
        imgs = self.get_uploads('Icon')

        #parse binaries blobstore
        for img in imgs:
            self.response.out.write('%s %s<br/>' % (img.filename,img.key()))

def main():
    application = webapp.WSGIApplication([('/.*', UploadBinary)],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
