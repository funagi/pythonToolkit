from google.appengine.ext import db,blobstore
from google.appengine.ext.db import Query
class AQIData(db.Model):
    City        = db.IntegerProperty()
    Station     = db.IntegerProperty()
    Date        = db.DateProperty()
    AQI         = db.IntegerProperty()
    AQILevel    = db.StringProperty()
    AQIAssess   = db.StringProperty()
    Majority    = db.StringProperty()

class Settings(db.Model):
    Name        = db.StringProperty()
    Value       = db.StringProperty()
    
class City(db.Model):
    Name        = db.StringProperty()
    Code        = db.IntegerProperty()

class Station(db.Model):
    Name        = db.StringProperty()
    Code        = db.IntegerProperty()
    City        = db.ReferenceProperty(City)
