from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from basetypes import *
import os, datetime, logging, json
from google.appengine.ext.db import Query

class Frame(webapp.RequestHandler):
    def get(self):
        template_values = {
            
            }
        path = os.path.join(os.path.dirname(__file__), './/template//frame.html')
        #----end------------------------------------------------------------------------------------------
        self.response.out.write(template.render(path,template_values))
        
class IndexNow(webapp.RequestHandler):
    def get(self):
        # List Cities
        citylist = {}
        cities = City.all()
        for city in cities:
            citylist[city.Name] = []
            for station in city.station_set:
                data = {'Name':station.Name}
                query = Query(AQIData)
                query.filter('Station =', station.Code)
                query.order('-Date')
                query.run()
                aqi = query.get()
                data['AQI'] = aqi.AQI
                data['Level'] = aqi.AQILevel
                data['Assess'] = aqi.AQIAssess
                citylist[city.Name].append(data)
        logging.info(str(citylist))
        #----generate parameter list----------------------------------------------------------------------
        template_values = {
            'citylist' : citylist,
            }
        path = os.path.join(os.path.dirname(__file__), './/template//citylist.html')
        #----end------------------------------------------------------------------------------------------
        self.response.out.write(template.render(path,template_values))


class IndexHistory(webapp.RequestHandler):
    def get(self):
        return

class FetchData(webapp.RequestHandler):
    def get(self):
        return

def main():
    application = webapp.WSGIApplication([
        (r'/query/data', FetchData),
        (r'/query/now', IndexNow),
        (r'/query/history', IndexHistory),
        (r'/.*', Frame)
        ],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
