from google.appengine.ext import db,blobstore

class game(db.Model):
    Id         = db.IntegerProperty()
    Name       = db.StringProperty()
    Company    = db.StringProperty()
    rDate      = db.DateProperty()
    pDate1     = db.DateProperty()
    pDate2     = db.DateProperty()
    Icon       = blobstore.BlobReferenceProperty()
    Poster     = blobstore.BlobReferenceProperty()
    Seiyuu     = db.TextProperty() 
    Memo       = db.TextProperty()
    Attachment = blobstore.BlobReferenceProperty()
    Hidden     = db.BooleanProperty(False)
    

