from basetypes import *
import logging,datetime
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import images

def pc_key(pc_name=None):
    if pc_name:
        return db.Key.from_path('Imageviewer', pc_name)
    else:
        return db.Key.from_path('Imageviewer', 'default')

class Upload(webapp.RequestHandler):
    def post(self):
        #get all the infomation
        str_time = self.request.get("time")
        str_pcname = self.request.get("PC")
        logging.info(str_time+' '+str_pcname)
        str_pic = self.request.get("data")

        #Check pc
        pclist = PCList().all().get()
        if not pclist:
            pclist = PCList(names=str_pcname+';')
            pclist.put()
        else:
            pc_list = pclist.names.split(';')
            if not (str_pcname in pc_list):
                pclist.names = pclist.names + str_pcname + ';'
                pclist.put()
        #Generate and put imgitem
        img_temp = imgitem(parent=pc_key(str_pcname))
        tempdate = datetime.datetime(2001, 1, 1, 0, 0)
        img_temp.time = tempdate.strptime(str_time, "%Y/%m/%d %H:%M:%S")
        img_temp.pc_name = str_pcname
        img_temp.data = str_pic

        #Generate thumbnail, width larger than height by default
        img_temp.thumb = images.resize(str_pic, 200, 150, images.JPEG)
        img_temp.put()
        self.response.out.write("200")
    def get(self):
        self.response.out.write("500")

def main():
    application = webapp.WSGIApplication([(r'/.*', Upload)],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
