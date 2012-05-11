from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from basetypes import *
import os,datetime,logging
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from google.appengine.dist import use_library
use_library('django', '0.96')

def pc_key(pc_name=None):
    if pc_name:
        return db.Key.from_path('Imageviewer', pc_name)
    else:
        return db.Key.from_path('Imageviewer', 'default')

def JudgeMobile(useragent):
    msys = ['iPhone','Symbian','Nokia','Mobile','HTC','J2ME','Opera Mini','MOT','SAMSUNG','JAVA']
    for sys in msys:
        if sys in useragent:
            return True
    return False
    
class ImageViewer(webapp.RequestHandler):
    def get(self):
        mobile = False
        #judge if mobile or not by user-agent
        useragent = self.request.headers.get('User-Agent')
        if JudgeMobile(useragent): mobile = True
        if mobile:
            countdefault = 10
        else:
            countdefault = 25
        off = self.request.get('offset',0)
        cnt = self.request.get('count',str(countdefault))  
        try:
            offset = int(off)
        except:
            offset = 0
        try:
            count = int(count)
        except:
            count = countdefault
            
        pc_name = self.request.get('pc')
        #----begin----------------------------------------------------------------------------------------
        imagedata = db.GqlQuery(
            'SELECT * FROM imgitem WHERE ANCESTOR IS :1 ORDER BY time DESC',
            pc_key(pc_name))
        logging.info('%s : %d ~ %d'%(pc_name,offset,offset+imagedata.count()))
        results = imagedata.fetch(count,offset)
        if len(results): self.error(404)
        #----end------------------------------------------------------------------------------------------
        #----devide into 5 x N----------------------------------------------------------------------------
        if not mobile:
            imagelist = []
            for i in range(0, len(results)/5+1):
                slist = []
                for j in range(0,5):
                    if j+i*5<len(results):
                        slist.append(results[j+i*5])
                imagelist.append(slist)
                    
        
        #----generate parameter list----------------------------------------------------------------------
        #if request from pc
        if not mobile:
            template_values = {
                'imagelist' : imagelist,
                'pc_name' : pc_name,
                'offset_next' : str(offset+countdefault),
                'offset_prev': str(max(offset-countdefault,0))
                }
            path = os.path.join(os.path.dirname(__file__), './/template//main.html')
        #if request from mobile
        else:
            template_values = {
                'imagelist' : imagedata,
                'pc_name' : pc_name,
                'offset_next' : str(offset+10),
                'offset_prev': str(max(offset-10,0))
                }
            path = os.path.join(os.path.dirname(__file__), './/template//main_wap.wml')
            self.response.headers['Content-Type']='text/vnd.wap.wml'
        #----end------------------------------------------------------------------------------------------
        self.response.out.write(template.render(path,template_values))


def main():
    application = webapp.WSGIApplication([(r'/.*', ImageViewer)],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
