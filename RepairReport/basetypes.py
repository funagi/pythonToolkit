from google.appengine.ext import db
from google.appengine.ext.db import Query
class Record(db.Model):
    Name        = db.StringProperty()
    CarNum      = db.StringProperty()
    Date        = db.DateProperty()
    Items       = db.StringListProperty()

    def getItems(self):
        return Items

class Item(db.Model):
    Order       = db.IntegerProperty()
    Name        = db.StringProperty()
    Number      = db.IntegerProperty()
    Unit        = db.StringProperty()
    Price       = db.FloatProperty()