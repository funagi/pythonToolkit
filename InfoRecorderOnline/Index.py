#encoding:utf-8
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from basetypes import *
import os,datetime,logging
    
class Frame(webapp.RequestHandler):
    def get(self):
        tablist = [
            {
                'destination' : '/main?ajax',
                'icon' : 'main',
                'tooltip' : ' 主界面 '
            },
            {
                'destination' : '/stat?ajax',
                'icon' : 'stat',
                'tooltip' : '统计信息'
            },
            {
                'destination' : '/show?ajax',
                'icon' : 'show',
                'tooltip' : '查看数据'
            },
            {
                'destination' : '/add?ajax',
                'icon' : 'add',
                'tooltip' : '添加数据'
            },
        ]
        #----generate parameter list----------------------------------------------------------------------
        template_values = {
            'tablist' : tablist
            }
        path = os.path.join(os.path.dirname(__file__), './/template//frame.html')
        #----end------------------------------------------------------------------------------------------
        self.response.out.write(template.render(path,template_values))


def main():
    application = webapp.WSGIApplication([(r'/.*', Frame)],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
