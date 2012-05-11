from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from basetypes import *

class Img(webapp.RequestHandler):
    def get(self):
        sid = self.request.get("id")
        if sid == '0':return
        img_temp = db.get(sid)
        if img_temp:
            self.response.headers['Content-Type'] = "image/png"
            self.response.out.write(img_temp.data)
        else:
            self.error(404)

def main():
    application = webapp.WSGIApplication([(r'/.*', Img)],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

