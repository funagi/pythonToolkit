from basetypes import *
import os,logging,datetime
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import search

class GamesList(webapp.RequestHandler):
    def get(self):
        gamelist = game.all()
        for gameitem in gamelist:
            for charaid in gameitem.Characters:
                chrquery = Query(Character)
                ch = chrquery.filter('cid =',charaid).get()
                if ch==None:
                    logging.error('non-exist cid : %d in game %s'%(charaid,gameitem.Name))
                else:
                    if str(gameitem.key()) not in ch.Games: 
                        ch.Games.append(str(gameitem.key()))
                        ch.put()
                    # 'no seiyuu' does not need a list
                    if ch.sid == 0:continue
                    # update seiyuu table
                    syquery = Query(Seiyuu)
                    sy = syquery.filter('sid =',ch.sid).get()
                    if sy==None:
                        logging.error('non-exist sid : %d in character %s (cid %d)'%(charaid,gameitem.Name,ch.cid))
                    else:
                        if str(gameitem.key()) not in sy.Games: 
                            sy.Games.append(str(gameitem.key()))
                            sy.put()
        # 'no seiyuu' should have an empty list
        syquery = Query(Seiyuu)
        sy = syquery.filter('sid =',0).get()
        sy.Games = []
        sy.put()
        logging.info(sy.Games)

        # setup seiyuu count
        slist = Seiyuu.all()
        for s in slist:
            if s.Games:
                s.GamesCount = len(s.Games)
            else:
                s.Games = []
                s.GamesCount = 0
            s.put()

class ClearSeiyuuList(webapp.RequestHandler):
    def get(self):
        slist = Seiyuu.all()
        for s in slist:
            s.Games = []
            s.GamesCount = 0
            s.put()

class IndexBuilder(webapp.RequestHandler):
    def get(self):
        indexname = self.request.get('name','')
        if indexname == 'game':
            # game index
            gmIndex = search.Index(name='Game')
            gamelist = game.all()
            for g in gamelist:
                company = db.get(g.Company).Name
                days = (g.pDate2-g.pDate1).days+1
                characters = []
                seiyuus = []
                romajis = []
                for chara in g.Characters:
                    chquery = Query(Character)
                    ch = chquery.filter('cid =', chara).get()
                    if ch!=None:
                        characters.append(ch.Name)
                        if ch.Romaji!=None: romajis.append(ch.Romaji)
                        syname = ch.getSeiyuuName()
                        mainname = ch.getMain()
                        if mainname!=None and mainname!=syname:
                            seiyuus.append('%s(%s)'%(syname,mainname))
                        else:
                            seiyuus.append(syname)
                    if g.Time == None:
                        time = 0
                    else:
                        time = g.Time
                    if g.Genre == None:
                        genre = ''
                    else:
                        genre = g.Genre
                gamedoc = search.Document(
                    fields=[search.TextField(name='Name', value=g.Name),
                            search.TextField(name='Company', value=company),
                            search.DateField(name='Release_Date', value=g.rDate),
                            search.DateField(name='Start_Date', value=g.pDate1),
                            search.DateField(name='Finish_Date', value=g.pDate2),
                            search.NumberField(name='Time', value=time),
                            search.TextField(name='Genre', value=g.Genre),
                            search.NumberField(name='Days', value=days),
                            search.TextField(name='Characters', value=' '.join(characters)),
                            search.TextField(name='Seiyuus', value=' '.join(seiyuus)),
                            search.TextField(name='Romajis', value=' '.join(romajis)),
                    ])
                try:
                    gmIndex.put(gamedoc)
                except:
                    logging.exception('Error putting a game document : name=%s'%g.Name)
                    return
        elif indexname == 'seiyuu':
            # seiyuu index
            syIndex = search.Index(name='Seiyuu')
            seiyuulist = Seiyuu.all()
            for seiyuu in seiyuulist:
                if seiyuu.isMain==None or seiyuu.isMain==False:
                    isMain = 0
                else:
                    isMain = 1
                charadoc = search.Document(
                    fields=[search.TextField(name='Name', value=seiyuu.Name),
                            search.NumberField(name='sid', value=seiyuu.sid),
                            search.NumberField(name='snum', value=seiyuu.snum),
                            search.TextField(name='Games', value=(' '.join([db.get(key).Name for key in seiyuu.Games]))),
                            search.NumberField(name='isMain', value=isMain),
                            search.NumberField(name='GamesCount', value=seiyuu.GamesCount),
                    ])
                try:
                    syIndex.put(charadoc)
                except:
                    logging.exception('Error putting a seiyuu document : sid=%d'%seiyuu.cid)
                    return
        elif indexname == 'character':
            # character index
            chrIndex = search.Index(name='Character')
            charalist = Character.all()
            for chara in charalist:
                if chara.Romaji == None:
                    romaji = ''
                else:
                    romaji = chara.Romaji
                if chara.getMain()==None:
                    main = ''
                else:
                    main = chara.getMain()
                charadoc = search.Document(
                    fields=[search.TextField(name='Name', value=chara.Name),
                            search.NumberField(name='cid', value=chara.cid),
                            search.NumberField(name='sid', value=chara.sid),
                            search.TextField(name='Romaji', value=romaji),
                            search.TextField(name='Seiyuu', value=chara.getSeiyuuName()),
                            search.TextField(name='SeiyuuMain', value=chara.getMain()),
                    ])
                try:
                    chrIndex.put(charadoc)
                except:
                    logging.exception('Error putting a character document : cid=%d'%chara.cid)
                    return

class IndexRemover(webapp.RequestHandler):
    def get(self):
        indexname = self.request.get('name','')
        if indexname != '' and indexname != 'all':
            index = search.Index(name=indexname)
            while True:
                ids = [document.doc_id for document in index.get_range(ids_only=True)]
                if not ids:
                    break
                index.delete(ids)

        elif indexname == 'all':
            indexes = ['Game','Seiyuu','Character']
            for iname in indexes:
                index = search.Index(name=iname)
                while True:
                    ids = [document.doc_id for document in index.get_range(ids_only=True)]
                    if not ids:
                        break
                    index.delete(ids)

def main():
    application = webapp.WSGIApplication([
        (r'/maintain/clearslist.*', ClearSeiyuuList),
        (r'/maintain/index.*', IndexBuilder),
        (r'/maintain/clearindex.*', IndexRemover),
        (r'/.*', GamesList)
        ],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
