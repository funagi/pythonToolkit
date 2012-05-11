from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from basetypes import *

class Thumb(webapp.RequestHandler):
    def get(self):
        img_temp = db.get(self.request.get("id"))
        if img_temp:
            self.response.headers['Content-Type'] = "image/jpeg"
            self.response.out.write(img_temp.thumb)
        else:
            self.error(404)

def main():
    application = webapp.WSGIApplication([(r'/.*', Thumb)],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

