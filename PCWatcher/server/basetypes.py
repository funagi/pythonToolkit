from google.appengine.ext import db

class imgitem(db.Model):
    time = db.DateTimeProperty()
    data = db.BlobProperty()
    pc_name = db.StringProperty()
    thumb = db.BlobProperty()

class PCList(db.Model):
    names = db.StringProperty()

