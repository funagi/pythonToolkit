from basetypes import *
import os,logging,datetime
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import blobstore_handlers

def datefromiso(isodate):
    y=int(isodate[:4])
    m=int(isodate[5:7])
    d=int(isodate[8:10])
    return datetime.date(y,m,d)
    
class Upload(webapp.RequestHandler):
    def get(self):
        uptype = self.request.get('type','')
        if uptype=='simple':
            template_values = {'upload_url' : blobstore.create_upload_url('/upload/simple')}
            path = os.path.join(os.path.dirname(__file__), './template/upload_simple.html')
        else:
            company2 = Company.all()
            company = []
            for com in company2:
                company.append({"key":com.key(),"Name":com.Name})
            template_values = {
            'upload_url' : blobstore.create_upload_url('/upload/bin'),
            'company' : company
            }
            path = os.path.join(os.path.dirname(__file__), './template/upload.html')
        self.response.out.write(template.render(path,template_values))

class UploadSimple(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        imgs = self.get_uploads('Icon')

        #parse binaries blobstore
        self.response.out.write('<html><body><div width=90% style="word-break:break-all;">')
        for img in imgs:
            logging.info(img.filename)
            filename = img.filename
            if filename[:2]=='=?':
                filenamearray = img.filename.split('?')
                filename = filenamearray[3].decode('base64').decode(filenamearray[1])
            self.response.out.write('%s %s<br/><hr>' % (filename,img.key()))
        self.response.out.write('</div></body></html>')

class UploadBinary(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        icon = self.get_uploads('Icon')[0]
        poster = self.get_uploads('Poster')[0]
        try:
            attachment = self.get_uploads('Attachment')[0]
        except:
            attachment = None

        #get all the infomation
        args = self.request.arguments()
        data = {}
        
        for arg in args:
            data[arg] = self.request.get(arg)
            
        #generate and put game object
        game_temp = game()
        #parse id
        # if ('Id' in data.keys()) and data['Id']=='':
        #     game_temp.Id = getLastId()
        # else:
        #     game_temp.Id = int(data['Id'])
        #parse strings
        game_temp.Name = data['Name'].decode('utf-8')
        logging.info(repr(data['Name']))
        game_temp.Company = data['Company'].decode('utf-8')
        chars = []
        for x in data['Characters'].split(','):
            if '-' in x:
                xs = x.split('-')
                chars += range(int(xs[0]),int(xs[1])+1)
            else:
                chars.append(int(x))
        game_temp.Characters = chars
        game_temp.ExtLinks = db.Text(data['Memo'])
        game_temp.VADB = int(data['VADB'])
        game_temp.VNDB = int(data['VNDB'])
        game_temp.EGS = int(data['EGS'])
        game_temp.Genre = unicode(data['Genre'])
        game_temp.Time = float(data['Time'])
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
        self.redirect('/main')

def main():
    application = webapp.WSGIApplication([
        (r'/upload/bin', UploadBinary),
        (r'/upload/simple', UploadSimple),
        (r'/upload', Upload),
        (r'.*', Upload)
        ],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
