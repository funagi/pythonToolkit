# coding = utf-8
import web,os,sqlite3,sys
#from web.wsgiserver import CherryPyWSGIServer
from web.contrib.template import render_mako

urls = (
    '/','Index',
    '/search','Search',
    '/icon','Icon'
    )
application = web.application(urls, globals(),autoreload=True).wsgifunc()
#app=web.wsgifunc(web.webpyfunc(urls, globals(),autoreload=True))
render = render_mako(directories=['.'],input_encoding='utf-8',output_encoding='utf-8')
#初始化SSL
#CherryPyWSGIServer.ssl_certificate = ".\\cert\\server.crt"
#CherryPyWSGIServer.ssl_private_key = ".\\cert\\server.key"
#初始化数据库
class sqldb:
    def __init__(self):
        print os.listdir('.')
        if os.path.exists('IndexLocal.db3'):
            self.conn = sqlite3.connect('IndexLocal.db3')
            self.c = self.conn.cursor()
        else:
            print os.listdir('.')
            return None


class Index:
    def GET(self):
        dbftp = sqldb()
        if dbftp:
            rec = dbftp.c.execute('''select * from db_ftp''')
            ftps = dbftp.c.fetchall()
            ftps2=[]
            for ftp in ftps:
                rec = dbftp.c.execute("SELECT COUNT(*) FROM sqlite_master where type='table' and name='"+ftp[0]+"'")
                exist = dbftp.c.fetchall()
                if (1,) in exist:
                    ftps2.append(ftp)
            return render.IndexWeb(ftps=ftps2,results=None,mode='query')
        else:
            return 'DataBase Lost!'
        
class Search:
    def POST(self):
        data = web.input(ftp=[])
        ftps = data['ftp']
        keyword = data['keyword']
        ftps2 = []
        dbftp = sqldb()
        
        if dbftp:
            for f in ftps:
                rec = dbftp.c.execute(u"select * from db_ftp where ftp_alias = '%s'" % f)
                ftps2 = ftps2 + dbftp.c.fetchall()
                
            results=[]
            for ftp in ftps2:
                rec = dbftp.c.execute("SELECT COUNT(*) FROM sqlite_master where type='table' and name='"+ftp[0]+"'")
                exist = dbftp.c.fetchall()
                if (1,) in exist:
                    rec = dbftp.c.execute('select * from '+ftp[0]+' where path like "%'+keyword+'%"')
                    results.append((ftp,dbftp.c.fetchall()))
                    #time.strptime(t,'%Y%m%d%H%M%S');time.strftime('%Y-%m-%d %H:%M:%S',s)
            return render.IndexWeb(ftps=ftps2,results=results,mode='list')


class Icon:
    def GET(self):
        web.header('content-type','image/x-icon')
        attr = web.input()['assoc']
        attr_list = {
            'dir' : ['dir'],
            'archive' : ['rar','zip','7z','bz2','gz'],
            'dll' : ['dll'],
            'document' : ['doc','rtf'],
            'excel' : ['xls','xlsx'],
            'execute' : ['exe','cmd','bat'],
            'image' : ['jpg','png','bmp','uci','ico'],
            'iso' : ['iso','mdf','mds','bin','img'],
            'video' : ['mkv','mp4','avi','ogm','flv','m2ts','mpg','rmvb','wmv'],
            'pdf' : ['pdf'],
            'sound' : ['wav','tta','tak','flac','ape','m4a','mp3','ogg','wma'],
            'text' : ['txt','srt','ssa','ass','log','cue','lrc'],
            'torrent' : ['torrent']
            }
        result = 'else'
        for type0 in attr_list:
            if attr.lower() in attr_list[type0]:
                result = type0

        fp = open('.//static//img//%s.ico' % result,'rb')
        return fp.read()
    
'''if __name__ == '__main__':
    #web.webapi.internalerror = web.debugerror
    #sys.args.append('1234')
    app.run()
    '''
