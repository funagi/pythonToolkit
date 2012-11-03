from google.appengine.ext import db,blobstore
from google.appengine.ext.db import Query
class game(db.Model):
    #ID          = db.IntegerProperty()
    Name        = db.StringProperty()
    Company     = db.StringProperty()
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
    EGS         = db.IntegerProperty(0)

    def getCharacters(self):
        return Seiyuu

    def getLinks(self):
        return ExtLinks

class Seiyuu(db.Model):
    sid         = db.IntegerProperty()
    snum        = db.IntegerProperty()
    Name        = db.StringProperty()
    isMain      = db.BooleanProperty(False)
    Games       = db.StringListProperty()
    GamesCount  = db.IntegerProperty()
    
class Character(db.Model):
    cid         = db.IntegerProperty()
    Name        = db.StringProperty()
    sid         = db.IntegerProperty()
    image       = blobstore.BlobReferenceProperty()
    Games       = db.StringListProperty()
    def getSeiyuuName(self):
        syquery = Query(Seiyuu)
        sy = syquery.filter('sid =',self.sid).get()
        if sy!=None:return sy.Name
    def getMain(self):
        syquery = Query(Seiyuu)
        syquery.filter('snum =',self.snum)
        syquery.filter('isMain = True')
        sy = syquery.get()
        if sy!=None:
            return sy.Name
        else:
            return None

class Company(db.Model):
    Name        = db.StringProperty()
    def getAllGames(self):
        glist = []
        query = Query(game)
        for g in query.filter('Company =',self.key()):
            glist.append(g.key())
        return glist