# encoding=utf-8

import sys,json,os,web,ctypes,re,sqlite3
from web.contrib.template import render_mako

def parsedata(data=[],num=20,sort=True):
    if sort:
        sortedkeys = sorted(data, key=data.__getitem__, reverse=True)
    else:
        data.keys().sort()
        sortedkeys = data.keys()
    sortedkeys = sortedkeys[:min(num,len(sortedkeys))]
    return sortedkeys

urls = (
    '/','Index',
    )

app = web.application(urls, globals(),autoreload=True)
render = render_mako(directories=['.'],input_encoding='utf-8',output_encoding='utf-8')
        
class Index:
    def GET(self):
        db = sqldb()
        # template = open('template.html','r').read()
        site_request={}
        site_size={}
        ip_request={}
        ip_size={}
        month_request={}
        month_size={}
        day_request={}
        day_size={}
        hour_request={}
        hour_size={}

        days = []
        hours = []
        months = []
        sites = []

        # ip rankings
        # get ip list
        c = db.cursor()
        c.execute("SELECT name FROM sqlite_master where type='table' and name LIKE 'ip\_%' ESCAPE '\\'")
        tablelist = c.fetchall()
        s = []
        for x in tablelist:
            # every ip is looped
            tablename = x[0]
            ip = '.'.join(tablename.split('_')[1:])
            # get total request and size
            c.execute("SELECT SUM(requests),SUM(size) FROM %s" % tablename)
            data = c.fetchone()

            ip_request[ip] = data[0]
            ip_size[ip] = data[1]
            # get data separately
            # days data and month data
            c.execute('''SELECT day,sum(size) AS totalsize,sum(requests) AS totalrequests FROM %s GROUP BY day ORDER BY day ASC''' % tablename)
            for data in c.fetchall():
                if data[0] in days:
                    day_request[data[0]] += data[2]
                    day_size[data[0]] += data[1]
                else:
                    days.append(data[0])
                    day_request[data[0]] = data[2]
                    day_size[data[0]] = data[1]

                if data[0]/100 in months:
                    month_request[data[0]/100] += data[2]
                    month_size[data[0]/100] += data[1]
                else:
                    months.append(data[0]/100)
                    month_request[data[0]/100] = data[2]
                    month_size[data[0]/100] = data[1]
            # hour data
            c.execute('''SELECT hour,sum(size) AS totalsize,sum(requests) AS totalrequests FROM %s GROUP BY hour ORDER BY hour ASC''' % tablename)
            for data in c.fetchall():
                if data[0] in hours:
                    hour_request[data[0]] += data[2]
                    hour_size[data[0]] += data[1]
                else:
                    hours.append(data[0])
                    hour_request[data[0]] = data[2]
                    hour_size[data[0]] = data[1]
            # site data
            c.execute('''SELECT site,sum(size) AS totalsize,sum(requests) AS totalrequests FROM %s GROUP BY site ORDER BY totalsize DESC LIMIT 100''' % tablename)
            for data in c.fetchall():
                if data[0] in sites:
                    site_request[data[0]] += data[2]
                    site_size[data[0]] += data[1]
                else:
                    sites.append(data[0])
                    site_request[data[0]] = data[2]
                    site_size[data[0]] = data[1]
        hours.sort()
        days.sort()
        months.sort()
        site_request_keys = parsedata(site_request)
        site_size_keys = parsedata(site_size)
        ip_size_keys = parsedata(ip_size, num=10)
        ip_request_keys = parsedata(ip_request, num=10)
        return render.Stats(ip_request=["['%s',%s]"%(x, ip_request[x]) for x in ip_request_keys],
                            ip_size=["['%s',%s]"%(x, ip_size[x]) for x in ip_size_keys],
                            hour_size=["[%d,%f,'%.2f']"%(x,float(hour_size[x])/(1024**3),float(hour_size[x])/(1024**3)) for x in hours],
                            hour_request=['[%d,%d]'%(x,hour_request[x]) for x in hours],
                            month_size=[["'%04d-%02d'"%(x/100,x%100) for x in months], [str(float(month_size[x])/(1024**3)) for x in months]],
                            month_request=[["'%04d-%02d'"%(x/100,x%100) for x in months], [str(month_request[x]) for x in months]],
                            day_size=["['%04d-%02d-%02d',%s]"%(x/10000,(x%10000)/100,x%100,str(float(day_size[x])/(1024**3))) for x in days],
                            # day_request=[["'%04d-%02d-%02d'"%(x/10000,(x%10000)/100,x%100) for x in days], [str(day_request[x]) for x in days]],
                            day_request=["['%04d-%02d-%02d',%s]"%(x/10000,(x%10000)/100,x%100,str(day_request[x])) for x in days],
                            site_size=[site_size_keys, [str(float(site_size[x])/(1024**3)) for x in site_size_keys]],
                            site_request=[site_request_keys, [str(site_request[x]) for x in site_request_keys]]
            )

class sqldb:
    def __init__(self):
        if os.path.exists('.\\privoxy.db3'):
            self.conn = sqlite3.connect('privoxy.db3')
            self.conn.text_factory = unicode
            self.cursor = self.conn.cursor
        else:
            return None

if __name__ == '__main__':
    # whnd = ctypes.windll.kernel32.GetConsoleWindow()  
    # if whnd != 0:  
    #     ctypes.windll.user32.ShowWindow(whnd, 0)  
    #     ctypes.windll.kernel32.CloseHandle(whnd)
    # # import ctypes
    # whnd = ctypes.windll.kernel32.GetConsoleWindow()
    # if whnd != 0:
    #     ctypes.windll.user32.ShowWindow(whnd, 0)
    #     ctypes.windll.kernel32.CloseHandle(whnd)
    app.run()
