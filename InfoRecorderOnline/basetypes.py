from google.appengine.ext import db,blobstore

class game(db.Model):
    ID          = db.IntegerProperty()
    Name        = db.StringProperty()
    Company     = db.IntegerProperty()
    rDate       = db.DateProperty()
    pDate1      = db.DateProperty()
    pDate2      = db.DateProperty()
    Icon        = blobstore.BlobReferenceProperty()
    Poster      = blobstore.BlobReferenceProperty()
    Characters  = db.ListProperty(int) 
    ExtLinks    = db.TextProperty()
    Attachment  = blobstore.BlobReferenceProperty()
    Hidden      = db.BooleanProperty(False)
    VNDB        = db.IntegerProperty(0)
    VADB        = db.IntegerProperty(0)

    def getSeiyuu(self):
        return Seiyuu

    def getLinks(self):
        return ExtLinks

class Seiyuu(db.Model):
    sid         = db.IntegerProperty()
    snum        = db.IntegerProperty()
    Name        = db.StringProperty()
    isMain      = db.BooleanProperty(False)
    
class Character(db.Model):
    cid         = db.IntegerProperty()
    Name        = db.StringProperty()
    sid         = db.IntegerProperty()
    image       = blobstore.BlobReferenceProperty()
    def getSeiyuuName(self):
        syquery = Query(Seiyuu)
        for sy in syquery.filter('sid =',self.sid):
            return sy.Name

class Company(db.Model):
    cpid        = db.IntegerProperty()
    Name        = db.StringProperty()