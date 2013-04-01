from basetypes import *
import os,logging,datetime,json
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

def datefromiso(isodate):
    y=int(isodate[:4])
    m=int(isodate[5:7])
    d=int(isodate[8:10])
    return datetime.date(y,m,d)

class Add(webapp.RequestHandler):
    def get(self):
        template_values = {
            }
        path = os.path.join(os.path.dirname(__file__), './template/upload.html')
        self.response.out.write(template.render(path,template_values))

    def post(self):
        #get all the infomation
        logging.info(self.request.arguments())
        jsondata = self.request.get('jsondata')
        logging.info(jsondata)
        data = json.loads(jsondata)
        #generate and put game object
        record_temp = Record()
        record_temp.Name = data['name'];
        record_temp.Date = datefromiso(data['date'])
        item_list = []
        count = 1
        for item in data['items']:
            item_temp = Item()
            item_temp.Name = item['name']
            item_temp.Number = int(item['num'])
            item_temp.Price = float(item['unitprice'])
            item_temp.Order = count
            count += 1
            key = item_temp.put()
            item_list.append(str(key))
        record_temp.Items = item_list
        record_temp.put()
        self.response.out.write('{"error":"no"}')
        # self.redirect('/main')

def main():
    application = webapp.WSGIApplication([
        (r'.*', Add)
        ],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
