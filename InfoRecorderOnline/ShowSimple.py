#encoding:utf-8
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext.db import BadKeyError
from basetypes import *
import os,datetime,logging,json

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
                    'serve_url' : '/show/game', 
                    'columns' : '7', 
                    'headers': ['图标', '名称', '会社', '发行日期', '开始日期', '结束日期', '编辑']
                    },
                'chara' : {
                    'serve_url' : '/show/chara', 
                    'columns' : '5', 
                    'headers': ['Image', 'CID', 'Name', 'Seiyuu', 'SID']
                    },
                'seiyuu' : {
                    'serve_url' : '/show/seiyuu', 
                    'columns' : '4', 
                    'headers': ['SID', 'Name', 'isMain', 'VADB Link']
                    },
                'comp' : {
                    'serve_url' : '/show/comp', 
                    'columns' : '2', 
                    'headers': ['序号', '名称']
                    },
                }

            if stat_type not in type_map.keys():
                self.error(404)
                return

            template_values = type_map[stat_type]

            path = os.path.join(os.path.dirname(__file__), './/template//show.html')
            self.response.out.write(template.render(path,template_values))

class ShowCharacters(webapp.RequestHandler):
    def get(self):
        charas = Character.all()

        charas.order('cid')

        datalist = []
        for chara in charas:
            datalist.append([
                '<img src="/data?key=%s" width=50 height=50/>' % chara.image.key(),
                chara.cid,
                chara.Name,
                chara.getSeiyuuName(),
                chara.sid
                ])

        #----end------------------------------------------------------------------------------------------
        jsondata = {
            'aaData' : datalist
        }
        self.response.out.write(json.dumps(jsondata))


class ShowSeiyuu(webapp.RequestHandler):
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

class ShowGame(webapp.RequestHandler):
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

class ShowCompany(webapp.RequestHandler):
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

def main():
    application = webapp.WSGIApplication([
        (r'/show', ShowCenter),
        (r'/show/chara', ShowCharacters),
        (r'/show/seiyuu', ShowSeiyuu),
        (r'/show/game', ShowGame),
        (r'/show/comp', ShowCompany),
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