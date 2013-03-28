#encoding:utf-8
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.api import search
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext.db import BadKeyError
from basetypes import *
import os,datetime,logging,json

class ShowCenterComplete(webapp.RequestHandler):
    def get(self):
        is_ajax = 'ajax' in self.request.arguments()

        stat_type = self.request.get('type','')
        if stat_type == '':
            template_values = {
                'title' : '查看数据',
                'ajax' : is_ajax,
                'tablist' : [
                    {'name' : '游戏', 'href' : '/show/complete?type=game'},
                    {'name' : '角色', 'href' : '/show/complete?type=chara'},
                    {'name' : '声优', 'href' : '/show/complete?type=seiyuu'},
                    {'name' : '会社', 'href' : '/show/complete?type=comp'},
                ],
                'type' : 'show'
            }
            path = os.path.join(os.path.dirname(__file__), './/template//tab.html')
            self.response.out.write(template.render(path,template_values))
            return
        else:
            type_map = {
                'game' : {
                    'serve_url' : '/show/complete/game', 
                    'columns' : '7', 
                    'headers': ['图标', '名称', '会社', '发行日期', '开始日期', '结束日期', '编辑'],
                    'serverside' : 'false'
                    },
                'chara' : {
                    'serve_url' : '/show/complete/chara', 
                    'columns' : '5', 
                    'headers': ['Image', 'CID', 'Name', 'Romaji', 'Seiyuu', 'SID', 'Action'],
                    'serverside' : 'false'
                    },
                'seiyuu' : {
                    'serve_url' : '/show/complete/seiyuu', 
                    'columns' : '4', 
                    'headers': ['SID', 'Name', 'isMain', 'VADB Link'],
                    'serverside' : 'false'
                    },
                'comp' : {
                    'serve_url' : '/show/complete/comp', 
                    'columns' : '2', 
                    'headers': ['序号', '名称'],
                    'serverside' : 'false'
                    },
                }

            if stat_type not in type_map.keys():
                self.error(404)
                return

            template_values = type_map[stat_type]

            path = os.path.join(os.path.dirname(__file__), './/template//show.html')
            self.response.out.write(template.render(path,template_values))

class ShowCharactersComplete(webapp.RequestHandler):
    def get(self):
        charas = Character.all()

        charas.order('cid')

        datalist = []
        for chara in charas:
            datalist.append([
                '<img src="/data?key=%s" width=50 height=50/>' % chara.image.key(),
                chara.cid,
                chara.Name,
                chara.Romaji,
                chara.getSeiyuuName(),
                chara.sid,
                '<a href="/edit/charadetail?key=%s">Edit</a>' % chara.key(),
                ])

        #----end------------------------------------------------------------------------------------------
        jsondata = {
            'aaData' : datalist
        }
        self.response.out.write(json.dumps(jsondata))

class ShowSeiyuuComplete(webapp.RequestHandler):
    def get(self):
        seiyuus = Seiyuu.all()
        seiyuus.order('sid')
        datalist = []
        for item in seiyuus:
            datalist.append([
                item.sid,
                item.Name,
                str(item.isMain),
                '<a href="http://beautyplanets.web.fc2.com/VADB/actor/c_%04d.html">%d</a>'%(item.snum,item.snum)
                ])

        jsondata = {
            'aaData' : datalist
        }

        self.response.out.write(json.dumps(jsondata))

class ShowGameComplete(webapp.RequestHandler):
    def get(self):
        games = game.all()
        games.order('rDate')
        datalist = []
        for item in games:
            datalist.append([
                '<img src="/data?key=%s" width=50 height=50/>'%item.Icon.key(),
                item.Name,
                db.get(item.Company).Name,
                item.rDate.strftime('%Y-%m-%d'),
                item.pDate1.strftime('%Y-%m-%d'),
                item.pDate2.strftime('%Y-%m-%d'),
                '<a href="/edit?key=%s">Edit</a><br/><a href="/edit/character?key=%s">Edit Characters</a>'%(item,item)
                ])

        jsondata = {
            'aaData' : datalist
        }

        self.response.out.write(json.dumps(jsondata))

class ShowCompanyComplete(webapp.RequestHandler):
    def get(self):
        comps = Company.all()
        comps.order('__key__')
        datalist = []
        i=1
        for comp in comps:
            datalist.append([
                i,
                comp.Name
                ])
            i+=1

        jsondata = {
            'aaData' : datalist
        }

        self.response.out.write(json.dumps(jsondata))

class ShowCenter(webapp.RequestHandler):
    def get(self):
        is_ajax = 'ajax' in self.request.arguments()

        stat_type = self.request.get('type','')
        if stat_type == '':
            template_values = {
                'title' : '查看数据',
                'ajax' : is_ajax,
                'tablist' : [
                    {'name' : '游戏', 'href' : '/show?type=game'},
                    {'name' : '角色', 'href' : '/show?type=chara'},
                    {'name' : '声优', 'href' : '/show?type=seiyuu'},
                    {'name' : '会社', 'href' : '/show?type=comp'},
                ],
                'type' : 'show'
            }
            path = os.path.join(os.path.dirname(__file__), './/template//tab.html')
            self.response.out.write(template.render(path,template_values))
            return
        else:
            type_map = {
                'game' : {
                    'serve_url' : '/show/search?type=Game', 
                    'columns' : '7', 
                    'headers': ['图标', '名称', '会社', '发行日期', '开始日期', '结束日期', '编辑'],
                    'serverside' : 'true'
                    },
                'chara' : {
                    'serve_url' : '/show/search?type=Character', 
                    'columns' : '5', 
                    'headers': ['Image', 'CID', 'Name', 'Romaji', 'Seiyuu', 'SID', 'Action'],
                    'serverside' : 'true'
                    },
                'seiyuu' : {
                    'serve_url' : '/show/search?type=Seiyuu', 
                    'columns' : '4', 
                    'headers': ['SID', 'Name', 'isMain', 'VADB Link'],
                    'serverside' : 'true'
                    },
                'comp' : {
                    'serve_url' : '/show/complete/comp', 
                    'columns' : '2', 
                    'headers': ['序号', '名称'],
                    'serverside' : 'false'
                    },
                }

            if stat_type not in type_map.keys():
                self.error(404)
                return

            template_values = type_map[stat_type]

            path = os.path.join(os.path.dirname(__file__), './/template//show.html')
            self.response.out.write(template.render(path,template_values))

class ShowSearch(webapp.RequestHandler):
    def get(self):
        type_map = {
            'Seiyuu': {
                'headers': ['sid','Name','isMain','snum','GamesCount'],
                'before' : ['', '', '', '', ''],
                'after'  : ['', '', '', '', '']
            },
            'Game': {
                #'headers':['Characters','Company','Days','Finish_Date','Genre','Name','Release_Date','Romajis','Seiyuus','Start_Date','Time'],
                'headers': ['Image','Name','Company','Release_Date','Days','Start_Date','Finish_Date','Genre','Time'],
                'before' : ['<img src="/data?key=', '', '', '', '', '', '', '', ''],
                'after'  : ['" width=50 height=50/>', '', '', '', '', '', '', '', '']
            },
            'Character': {
                'headers': ['Image','cid','Name','Romaji','Seiyuu','SeiyuuMain','sid'],
                'before' : ['<img src="/data?key=', '', '', '', '', '', '<a href="/edit/charadetail?key='],
                'after'  : ['" width=50 height=50/>', '', '', '', '', '', '">Edit</a>']
            },
        }
        sortdir_map = {
            'asc' : search.SortExpression.ASCENDING,
            'desc': search.SortExpression.DESCENDING
        }
        # if len(colinfo['headers'])!=len(colinfo['before']) || len(colinfo['headers'])!=len(colinfo['after']):
        #     return
        index_name = self.request.get('type','')
        keyword = self.request.get('sSearch','')
        sEcho = self.request.get('sEcho',0)
        sort = self.request.get('iSortingCols','1')
        sortdir = self.request.get('sSortDir','asc')
        charas = Character.all()
        iTotalRecords = charas.count()
        iDisplayRecords = 0
        start = self.request.get('iDisplayStart','0')
        count = self.request.get('iDisplayLength','10')

        colinfo = type_map[index_name]
        try:
            index = search.Index(index_name)
            options = search.QueryOptions(
                limit=int(count), 
                offset=int(start),
                sort_options=search.SortOptions(expressions=[search.SortExpression(
                        expression=colinfo['headers'][int(sort)],
                        direction=sortdir_map[sortdir]
                    )])
                )
            query = search.Query(keyword, options)
            results = index.search(query)
            iDisplayRecords = results.number_found
        except search.Error:
            logging.exception('Search %s Failed: %s'%(index_name, keyword))

        datalist = []
        logging.info('%s : %d'%(keyword, results.number_found))
        for res in results:
            entry = []
            for column in colinfo['headers']:
                i = colinfo['headers'].index(column)
                entry.append( colinfo['before'][i] + unicode(res.field(column).value) + colinfo['after'][i] )
            datalist.append(entry)

        #----end------------------------------------------------------------------------------------------
        jsondata = {
            'sEcho' : int(sEcho),
            'iTotalRecords' : iTotalRecords,
            'iTotalDisplayRecords' : iDisplayRecords,
            'aaData' : datalist
        }
        self.response.out.write(json.dumps(jsondata))

def main():
    application = webapp.WSGIApplication([
        (r'/show', ShowCenter),
        (r'/show/complete', ShowCenterComplete),
        (r'/show/complete/chara', ShowCharactersComplete),
        (r'/show/complete/seiyuu', ShowSeiyuuComplete),
        (r'/show/complete/game', ShowGameComplete),
        (r'/show/complete/comp', ShowCompanyComplete),
        (r'/show/search', ShowSearch),
        (r'/show.*', ShowCenter)
        ],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
'''
sEcho = self.request.get('sEcho')
        charas = Character.all()
        iTotalRecords = charas.count()
        start = self.request.get('iDisplayStart','0')
        count = self.request.get('iDisplayLength','10')
        iSortCol_0 = int(self.request.get('iSortCol_0','1'))
        sSortDir_0 = self.request.get('sSortDir_0','asc')
        data_rows = ['','cid','Name','','sid']
        sort = data_rows[iSortCol_0]
        if sort=='':
            sort = data_rows[1]
        if sSortDir_0=='desc':
            sort = '-'+sort

        charas.order(sort)

        datalist = []
        for chara in charas.fetch(int(count),offset=int(start)):
            datalist.append([
                '<img src="/data?key=%s" width=50 height=50/>' % chara.image.key(),
                chara.cid,
                chara.Name,
                chara.getSeiyuuName(),
                chara.sid
                ])

        #----end------------------------------------------------------------------------------------------
        jsondata = {
            'sEcho' : int(sEcho),
            'iTotalRecords' : iTotalRecords,
            'iTotalDisplayRecords' : iTotalRecords,
            'aaData' : datalist
        }
        self.response.out.write(json.dumps(jsondata))
'''