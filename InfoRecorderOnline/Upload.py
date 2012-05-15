from basetypes import *
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class Upload(webapp.RequestHandler):
    def get(self):
        self.response.out.write('upload_url')
        template_values = {'upload_url' : blobstore.create_upload_url('/upload/bin')}
        path = os.path.join(os.path.dirname(__file__), './template/upload.html')
        self.response.out.write(template.render(path,template_values))

def main():
    application = webapp.WSGIApplication([('/.*', Upload)],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
