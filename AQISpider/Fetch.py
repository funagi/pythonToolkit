from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from basetypes import *
import os, datetime, logging, json
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from google.appengine.ext.db import Query
from google.appengine.api.urlfetch import fetch, create_rpc, make_fetch_call, DownloadError

class Fetch(webapp.RequestHandler):
    def get(self):
        # URL Pattern
        url = r"http://218.94.78.75/newrest/REST/V100/STATION/32/AQI/DAYNOW?token=%s"
        # Generate Token
        sha = SHA256.new()
        sha.update(str(datetime.datetime.now()))
        token = sha.hexdigest()
        token = token[:32].lower()

        # Fetch Content
        rpc = create_rpc()
        make_fetch_call(rpc, url % token)
        try:
            result = rpc.get_result()
            if result.status_code == 200:
                base64 = result.content
            else:
                raise DownloadError()
        except DownloadError,e:
            logging.error('Download Error: %s' % str(e))
            return

        # Parse Content
        newtoken = token.replace(token[0], 't')
        sha = SHA256.new()
        sha.update(newtoken)
        newtoken = sha.digest()
        key = newtoken
        vec = newtoken[16:]
        # logging.info("token: %s" % token)
        # logging.info("key: %s ; vector: %s" % (key,vec))
        crypt = AES.new(key, AES.MODE_CBC, vec)
        jsondata = crypt.decrypt(base64.decode('base64'))
        jsondata = jsondata.decode('utf-8')
        logging.info(token)
        # self.response.out.write(jsondata)

        try:
            data = json.loads(jsondata)
        except:
            # return
            jsondata = jsondata.replace(jsondata[len(jsondata)-1],'')
            data = json.loads(jsondata)

        month = data['month']
        day = data['day']
        year = data['year']

        datequery = AQIData.all()
        datequery.order('-Date')
        item = datequery.get()
        if item!= None and item.Date==datetime.date(int(year),int(month),int(day)):
            logging.info('Old data for %4d-%02d-%02d'%(int(year),int(month),int(day)));
            return

        logging.info('Updating data for %4d-%02d-%02d, %d entries'%(int(year),int(month),int(day),len(data['data'])));
        for entry in data['data']:
            dbentry = AQIData()
            dbentry.City = int(entry['xzqdm'])
            dbentry.Station = int(entry['zddm'])
            dbentry.Date = datetime.date(int(year),int(month),int(day))
            dbentry.AQI = int(entry['aqiz'])
            dbentry.AQILevel = entry['aqidj']
            dbentry.AQIAssess = entry['aqipd']
            dbentry.Majority = entry['sywrw']
            dbentry.put()

class UpdateAlias(webapp.RequestHandler):
    def get(self):
        # URL Pattern
        url = r"http://218.94.78.75/newrest/REST/V100/STATION/32/AQI/DAYNOW?token=%s"
        # Generate Token
        sha = SHA256.new()
        sha.update(str(datetime.datetime.now()))
        token = sha.hexdigest()
        token = token[:32].lower()

        # Fetch Content
        rpc = create_rpc()
        make_fetch_call(rpc, url % token)
        try:
            result = rpc.get_result()
            if result.status_code == 200:
                base64 = result.content
            else:
                raise DownloadError()
        except DownloadError,e:
            logging.error('Download Error: %s' % str(e))
            return

        # Parse Content
        newtoken = token.replace(token[0], 't')
        sha = SHA256.new()
        sha.update(newtoken)
        newtoken = sha.digest()
        key = newtoken
        vec = newtoken[16:]
        # logging.info("token: %s" % token)
        # logging.info("key: %s ; vector: %s" % (key,vec))
        crypt = AES.new(key, AES.MODE_CBC, vec)
        jsondata = crypt.decrypt(base64.decode('base64'))
        jsondata = jsondata.decode('utf-8')
        logging.info(token)
        # self.response.out.write(jsondata)

        try:
            data = json.loads(jsondata)
        except:
            # return
            jsondata = jsondata.replace(jsondata[len(jsondata)-1],'')
            data = json.loads(jsondata)

        citylist = {}
        cityobj = {}
        stationlist = {}
        for entry in data['data']:
            citylist[entry['xzqdm']] = entry['xzqmc']
            stationlist[entry['zddm']] = entry['zdmc']

        for city in citylist:
            ncity = City()
            ncity.Name = citylist[city]
            ncity.Code = int(city)
            ncity.put()
            cityobj[city] = ncity

        for entry in data['data']:
            nstation = Station()
            nstation.Name = entry['zdmc']
            nstation.Code = int(entry['zddm'])
            nstation.City = cityobj[entry['xzqdm']]
            nstation.put()

def main():
    application = webapp.WSGIApplication([
        (r'/fetch/alias', UpdateAlias),
        (r'/.*', Fetch)
        ],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
