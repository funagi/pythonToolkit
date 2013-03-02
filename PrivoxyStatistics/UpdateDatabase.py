#encoding: utf-8
import sys,json,os,web,ctypes,re,sqlite3
db = sqlite3.connect('privoxy.db3')
db.text_factory = unicode

def putData(cursor, ip, site, day, hour, size, requests):
    ip = ip.replace('.','_')    
    cursor.execute("INSERT INTO ip_%s VALUES ('%s',%d,%d,%d,%d)" % (ip, site, day, hour, size, requests))


c = db.cursor()
# c.execute('create table visits (ip TEXT, site TEXT, date INT, size INT, requests INT)')
regex = re.compile(r'(?P<ip>[0-9\.]+) - - \[(?P<day>[0-9]{2})/(?P<month>[A-Za-z]{3})/(?P<year>[0-9]{4}):(?P<hour>[0-9]{2}):[0-9]{2}:[0-9]{2} \+[0-9]{4}\] "(?P<method>[A-Z]+) (?P<address>.+) HTTP/1.1" [0-9]{3} (?P<size>\d+)')
regex_site = re.compile(r'((http(s|)://|)(?P<site>.+?)(:\d+|/.*))')
monthmap = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12',}

count = 0

LogFile = open('Privoxy3.log')
ips = {}
for line in LogFile:
    sch = regex.search(line)
    if sch:
        # gather information
        ip = sch.group("ip")
        hour = int(sch.group("hour"))
        address = sch.group("address")
        size = int(sch.group("size"))
        year = sch.group("year")
        month = sch.group("month")
        day = sch.group("day")
        date = int(year+monthmap[month]+day)
        sitesch = regex_site.search(address)
        if sitesch==None:
            print line
            continue
        else:
            site = sitesch.group('site')

        # parse information
        if not ip in ips.keys():
            ips[ip] = {
                (site, date, hour) : {'size': size, 'request': 1},
                }
        else:
            data = ips[ip]
            if (site, date, hour) in data.keys():
                ips[ip][(site, date, hour)]['size'] += size
                ips[ip][(site, date, hour)]['request'] += 1
            else:
                ips[ip][(site, date, hour)] = {'size': size, 'request': 1}
        count += 1
        # if count >= 200000: break
        if count%100000==0: print count

# write into database
for key in ips.keys():
    c = db.cursor()
    # see if database exists
    c.execute("SELECT COUNT(*) FROM sqlite_master where type='table' and name='ip_" + key.replace('.','_')+"'")
    exist = c.fetchall()
    if not (1,) in exist:
        c.execute('create table ip_'+key.replace('.','_')  +' (site TEXT, day INT, hour INT, size INT, requests INT)')
        db.commit()
    c.close()
    c = db.cursor()
    # insert entries
    for entry in ips[key].keys():
        putData(c, key, entry[0], entry[1], entry[2], ips[key][entry]['size'], ips[key][entry]['request'])
    db.commit()
    c.close()
print count
os.system('pause')