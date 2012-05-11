# coding = utf-8
import ftplib,sqlite3
import re,os

'''os.system('FTP Index Generator')'''
errors = 0 #错误数目
counts = 0 #目录数目
def Path(info):
    if(info[3]==''):
        return 'ftp://'+info[1]+':'+str(info[2])
    else:
        return 'ftp://'+info[3]+':'+info[4]+'@'+info[1]+':'+str(info[2])

def Walk (path):
    try:
        print path
        global counts,errors;counts+=1
        temp=[]
        stage=0
        #specially for xeochen
        #if counts >=60: connection.retrlines('RETR "./三牛的五花八门 2011.02.22.txt"'.encode('gb18030'),temp.append);counts=0
        locallist = []
        dirlist = []
        #path = path.decode('gbk')
        stat = connection.retrlines('MLSD '+path,locallist.append)
        stage=1
        #path = path.decode('gb18030')
        re_type = re.compile(ur'(?<=type=)\w+(?=;)')
        re_date = re.compile(ur'(?<=(modified)=)\d+(?=;)')
        re_date2 = re.compile(ur'(?<=(modify)=)\d+(?=;)')
        re_size = re.compile(ur'(?<=size=)\w+(?=;)')
        if stat[:3]=='226':
            for localline in locallist:
                stage=2
                localline = localline.decode('utf-8')
                stage=3
                if u'modified' in localline:
                    date = re_date.search(localline).group(0)
                else:
                    date = re_date2.search(localline).group(0)
                    
                if u'type=dir' in localline:
                    dirlist.append(localline[localline.rindex('; ')+2:])
                    fp = path.decode('gbk')+'/'+localline[localline.rindex('; ')+2:]
                    c.execute(u'insert into '+site[0]+u' values (?,?,?,?)',(u'd',fp,date,0))
                elif u'type=file' in localline:
                    size = re_size.search(localline).group(0)
                    fp = path.decode('gbk')+'/'+localline[localline.rindex('; ')+2:]
                    c.execute(u'insert into '+site[0]+u' values (?,?,?,?)',(u'f',fp,date,size))
            for dirs in dirlist:
                stage=4
                pathtemp = (path.decode('gbk')+'/'+dirs)
                
                Walk(pathtemp.encode('gbk'))
            db.commit()
        else:
            print site,path,stat
    except Exception as e:
        print '********************************************************************'
        errors+=1
        if 'fp' in dir():print 'fp:',fp
        if 'site' in dir():print 'site:',site
        if 'localline' in dir():print 'localline:',repr(localline)
        if 'site' in dir():print 'site:',site
        if 'path' in dir():print 'path:',repr(path)
        if 'stat' in dir():print 'stat:',stat
        if 'e' in dir():print 'e:',e
        if 'e' in dir():print 'stage:',stage
        #if 'exit' in raw_input():c.close();connection.quit()

if __name__ == '__main__':
    db = sqlite3.connect('IndexLocal.db3')
    db.text_factory = unicode
    c = db.cursor()
    c.execute('select * from db_ftp order by ftp_alias')
    site_list = c.fetchall()
    c.close()
    #选择分支
    print '----------------------------------------------------------------'
    print '0 Scan All Ftps'
    for i in range(0,len(site_list)):
        print str(i+1),Path(site_list[i])
    print '''----------------------------------------------------------------'''
    s = raw_input('Please select, or Press Enter to exit:')
    if s=='0':
        connection = ftplib.FTP()
        for site in site_list:
            print '----------------------------------------------------------------'
            #print site
            connection.connect(site[1],site[2])
            if(site[3]==''):
                connection.login()
                print 'Scanning Directories on ftp://'+site[1]+':'+str(site[2])
            else:
                connection.login(site[3],site[4])
                print 'Scanning Directories on ftp://'+site[3]+':'+site[4]+'@'+site[1]+':'+str(site[2])
            #检测数据表存在性
            c = db.cursor()
            c.execute("SELECT COUNT(*) FROM sqlite_master where type='table' and name='"+site[0]+"'")
            exist = c.fetchall()
            if (1,) in exist:
                c.execute('drop table '+site[0])
            c.execute('create table '+site[0]+' (type TEXT, path TEXT UNIQUE, modified INT, size INT)')
            db.commit()
            #开始列目录
            Walk('.')
            c.close()
        connection.quit()
        print '----------------------------------------------------------------'
        print 'Scanning Finished!'
    elif int(s)>0 and int(s)<=len(site_list):
        site = site_list[int(s)-1]
        connection = ftplib.FTP()
        print '----------------------------------------------------------------'
        #print site
        connection.connect(site[1],site[2])
        if(site[3]==''):
            connection.login()
            print 'Scanning Directories on ftp://'+site[1]+':'+str(site[2])
        else:
            connection.login(site[3],site[4])
            print 'Scanning Directories on ftp://'+site[3]+':'+site[4]+'@'+site[1]+':'+str(site[2])
        #检测数据表存在性
        c = db.cursor()
        c.execute("SELECT COUNT(*) FROM sqlite_master where type='table' and name='"+site[0]+"'")
        exist = c.fetchall()
        if (1,) in exist:
            c.execute('drop table '+site[0])
        c.execute('create table '+site[0]+' (type TEXT, path TEXT UNIQUE, modified INT, size INT)')
        db.commit()
        Walk('.')
        c.close()
        connection.quit()
        print '----------------------------------------------------------------'
        print 'Scanning Finished with %d errors.' % errors
    raw_input('Press enter to exit.....')
