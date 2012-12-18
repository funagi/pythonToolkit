#encoding:utf-8
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext.db import BadKeyError
from basetypes import *
import os,datetime,logging
from operator import itemgetter
    
class StatGame(webapp.RequestHandler):
    def get(self):
        is_ajax = 'ajax' in self.request.arguments()

        stat_type = self.request.get('type','')
        if stat_type == '':
            template_values = {
                'title' : '统计信息',
                'ajax' : is_ajax,
                'tablist' : [
                    {'name' : '发行年', 'href' : '/stat?type=ryear'},
                    {'name' : '开始年份', 'href' : '/stat?type=pyear'},
                    {'name' : '开始月份', 'href' : '/stat?type=pmonth'},
                    {'name' : '会社', 'href' : '/stat?type=comp'},
                    {'name' : '角色人数分布', 'href' : '/stat?type=chara'},
                    {'name' : '游戏时间分布', 'href' : '/stat?type=days'}
                ],
                'type' : 'stat'
            }
            path = os.path.join(os.path.dirname(__file__), './/template//tab.html')
            self.response.out.write(template.render(path,template_values))
            return

        games = game.all()

        if stat_type=='ryear':
            datalist_temp = {}
            for g in games:
                ryear = g.rDate.year
                if ryear not in datalist_temp.keys():
                    datalist_temp[ryear] = 1
                else:
                    datalist_temp[ryear] += 1
            datalist = sorted(datalist_temp.iteritems(), key=itemgetter(0), reverse=False)

        elif stat_type=='pyear':
            datalist_temp = {}
            for g in games:
                pyear = g.pDate1.year
                if pyear not in datalist_temp.keys():
                    datalist_temp[pyear] = 1
                else:
                    datalist_temp[pyear] += 1
            datalist = sorted(datalist_temp.iteritems(), key=itemgetter(0), reverse=False)

        elif stat_type=='pmonth':
            datalist_temp = {}
            for g in games:
                pmonth = '%04d-%02d' % (g.pDate1.year,g.pDate1.month)
                if pmonth not in datalist_temp.keys():
                    datalist_temp[pmonth] = 1
                else:
                    datalist_temp[pmonth] += 1
            datalist = sorted(datalist_temp.iteritems(), key=itemgetter(0), reverse=False)

        elif stat_type=='comp':
            datalist_temp = {}
            for g in games:
                comp = db.get(g.Company).Name
                if comp not in datalist_temp.keys():
                    datalist_temp[comp] = 1
                else:
                    datalist_temp[comp] += 1
            datalist = sorted(datalist_temp.iteritems(), key=itemgetter(1), reverse=True)

        elif stat_type=='chara':
            datalist = []
            for g in games:
                datalist.append(len(g.Characters))

        elif stat_type=='days':
            datalist = []
            for g in games:
                datalist.append((g.pDate2-g.pDate1).days)

        else:
            self.error(404)
            return

        type_map = {
            'ryear' : {'caption' : '发行年', 'data' : datalist, 'type' : 'bar', 'name' : 'ryear'},
            'pyear' : {'caption' : '开始年份', 'data' : datalist, 'type' : 'bar', 'name' : 'pyear'},
            'pmonth' : {'caption' : '开始月份', 'data' : datalist, 'type' : 'bar', 'name' : 'pmonth'},
            'comp' : {'caption' : '会社', 'data' : datalist, 'type' : 'bar', 'name' : 'comp'},
            'chara' : {'caption' : '角色人数分布', 'data' : datalist, 'type' : 'hist', 'name' : 'chara'},
            'days' : {'caption' : '游戏时间分布', 'data' : datalist, 'type' : 'hist', 'name' : 'days'}
            }

        template_values = type_map[stat_type]

        path = os.path.join(os.path.dirname(__file__), './/template//statistics.html')
        self.response.out.write(template.render(path,template_values))


def main():
    application = webapp.WSGIApplication([
        (r'/.*', StatGame)
        ],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
