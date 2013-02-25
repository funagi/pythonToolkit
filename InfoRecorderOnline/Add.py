#encoding:utf-8
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from basetypes import *
import os,datetime,logging,json

class AddCenter(webapp.RequestHandler):
    def get(self):
        is_ajax = 'ajax' in self.request.arguments()

        stat_type = self.request.get('type','')
        if stat_type == '':
            template_values = {
                'title' : '添加数据',
                'ajax' : is_ajax,
                'tablist' : [
                    {'name' : '角色', 'href' : '/add?type=chara'},
                    {'name' : '声优', 'href' : '/add?type=seiyuu'},
                    {'name' : '会社', 'href' : '/add?type=comp'},
                    {'name' : '游戏', 'href' : '/upload'},
                    {'name' : '文件', 'href' : '/upload?type=simple'},
                ],
                'type' : 'add'
            }
            path = os.path.join(os.path.dirname(__file__), './/template//tab.html')
            self.response.out.write(template.render(path,template_values))
            return
        else:
            type_map = {
                'chara' : {
                    'name' : 'chara',
                    'submit_url' : '/add/character', 
                    'hint1' : 'Name, Romaji, sid, imagekey',
                    'hint2' : 'AMIfv95okg1m9KhvbYhXEHcqEhnOflFSj4paCzbWDq_qDwjvuK-_rYsgveF5ehqMp-rmxZfuYC47x4kXmkrfTcdfJ2u4O3aYAuNaHZoKi8QfhrSLN_xMsd7tjgtGxkdEQkp-JzZjqR0Cd5gMWesygGikVUEljJFCRQ'
                    },
                'seiyuu' : {
                    'name' : 'seiyuu',
                    'submit_url' : '/add/seiyuu', 
                    'hint1' : 'Name,snum,isMain',
                    'hint2' : ''
                    },
                'comp' : {
                    'name' : 'comp',
                    'submit_url' : '/add/company', 
                    'hint1' : '',
                    'hint2' : ''
                    },
                }

            if stat_type not in type_map.keys():
                self.error(404)
                return

            template_values = type_map[stat_type]

            path = os.path.join(os.path.dirname(__file__), './/template//add.html')
            self.response.out.write(template.render(path,template_values))

class AddCharacter(webapp.RequestHandler):
    def post(self):
        rawdata = self.request.get('text').replace('\r\n','\n')
        # get latest id
        dbquery = db.GqlQuery('SELECT * FROM Character ORDER BY cid DESC')
        if dbquery.fetch(1):
            new_id = dbquery.fetch(1)[0].cid+1
        else:
            new_id = 1
        id_backup = new_id
        for dataline in rawdata.split('\n'):
            data = dataline.split(',')
            newchara = Character()
            newchara.Name = data[0]
            newchara.Romaji = data[1]
            newchara.sid = int(data[2])
            
            newchara.cid = new_id
            newchara.image = data[3]
            newchara.put()
            new_id += 1
            # else:
            #     continue
        self.response.out.write(json.dumps({'number':new_id-id_backup}))
        return

class AddCompany(webapp.RequestHandler):
    def post(self):
        rawdata = self.request.get('text').replace('\r\n','\n')
        for dataline in rawdata.split('\n'):
            logging.info(repr(dataline))
            compinfo = db.GqlQuery("SELECT * FROM Company WHERE Name='%s'"% dataline)
            result = compinfo.fetch(1)
        
            if len(result)==0 and dataline!='': 
                newcomp = Company()
                newcomp.Name = dataline
                newcomp.put()
            else:
                continue
        self.response.out.write(json.dumps({'number':len(rawdata.split('\n'))}))
        return

class AddSeiyuu(webapp.RequestHandler):
    def post(self):
        rawdata = self.request.get('text').replace('\r\n','\n')
        # get latest id
        dbquery = db.GqlQuery('SELECT * FROM Seiyuu ORDER BY sid DESC')
        if dbquery.fetch(1):
            new_id = dbquery.fetch(1)[0].sid+1
        else:
            new_id = 1
        id_backup = new_id
        for dataline in rawdata.split('\n'):
            data = dataline.split(',')
            charainfo = db.GqlQuery("SELECT * FROM Seiyuu WHERE Name='%s' AND snum=%s"% (data[0], data[1]))
            result = charainfo.fetch(1)
        
            if len(result)==0: 
                newseiyuu = Seiyuu()
                newseiyuu.Name = data[0]
                newseiyuu.snum = int(data[1])
                if data[2]=="1":
                    newseiyuu.isMain = True
                else:
                    newseiyuu.isMain = False
                
                newseiyuu.sid = new_id
                newseiyuu.put()
                new_id += 1
            else:
                continue
        self.response.out.write(json.dumps({'number':new_id-id_backup}))
        return

def main():
    application = webapp.WSGIApplication([
        (r'/add', AddCenter),
        (r'/add/character', AddCharacter),
        (r'/add/seiyuu', AddSeiyuu),
        (r'/add/company', AddCompany),
        (r'.*', AddCharacter)
        ],debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
