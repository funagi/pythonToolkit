from google.appengine.ext import webapp
from google.appengine.ext import blobstore
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import blobstore_handlers
from basetypes import *
import logging,datetime

class DataServe(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):#, data_key):
        self.response.headers.add_header('Expires',(datetime.datetime.today()+datetime.timedelta(weeks=1)).strftime('%H:%M:%S-%a/%d/%b/%Y'))
        try:
            data_key = self.request.get('key')
            blob = blobstore.get(data_key)
            if not blob:
                self.error(404)
            else:
                self.send_blob(blob)
                logging.info(blob.size)
        except:
            logging.error(data_key)

def main():
    application = webapp.WSGIApplication([(r'/.*', DataServe)],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

