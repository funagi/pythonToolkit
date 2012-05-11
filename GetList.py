from HTMLParser import HTMLParser
import re
fp = open('index.htm','r')

l = []
class GetTorrentList(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.flag = 0
        self.tag = ''
        self.TorrentList = []

    def handle_starttag(self,tag,attrs):
        '''if tag == 'tr':
            for (variable, value) in attrs:
                if variable == 'class' and value[:8] == 'windowbg':
                    self.flag = 1
                    self.tag = tag
                    #print self.get_starttag_text()'''
        if tag == 'td':
            for (variable, value) in attrs:
                if not(variable == 'id' and value == 'sp_center'):
                    self.flag = 2
                    self.tag = tag
        if tag == 'div':
            for (variable, value) in attrs:
                if variable == 'class' and value == 'pagesection':#navPages':
                    self.flag = 0

    def handle_data(self,data):
        if self.flag == 2:
            l.append(data)

    

if __name__ == '__main__':
    cleaner = re.compile(r'\t|\n|&#\d+;')
    code = fp.read()
    code = re.sub(cleaner,'',code)
    f = open('w.txt','w')
    f.write(code)
    f.close()
    code = code.replace('torrent=0"><','torrent=0">Null<')
    hp = GetTorrentList()
    hp.feed(code)
    hp.close()
    o = []
    
    for i in range(0,len(l)-1,6):
        o.append([l[i],l[i+1],l[i+2],l[i+3],l[i+4],l[i+5]])
    print o
