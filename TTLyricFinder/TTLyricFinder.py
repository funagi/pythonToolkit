import urllib,jianfan,json
import xml.etree.ElementTree as ET
from Tkinter import *


def Encode(string):
    out = u''
    if type(string) != unicode:
        string = unicode(string,'gbk')
    for word in string:
        h = '%04X'%ord(word)
        out += (h[2:]+h[:2])
    return out

def GetQuery(singer, title):
    result = []#查询结果
    s = Encode(singer.lower())
    t = Encode(title.lower())
    print s,t
    url = 'http://ttlrccnc.qianqian.com/dll/lyricsvr.dll?sh?Artist='+s+'&Title='+t\
        +'&Flags=0&ci=545b5b56544d436111147132492b345316101c02111c6d5c252a265b534644141c464808425c5353011d01'
    socks = urllib.urlopen(url)
    xml = socks.read()
    xml = xml.decode('utf-8')
    xmltree = ET.fromstring(xml)
    lrcs = xmltree.findall('lrc')
    for lrc in lrcs:
        dat = lrc.items()
        result.append((dat[0][1],dat[2][1],dat[1][1]))
    return result
    
def GetCode(singer, title, lrcid):
    HexStr = Encode(singer+title)
    print HexStr
    length = len(HexStr) / 2
    song = [int(HexStr[i*2:i*2+2],16) for i in range(0,length)]

    t1 = (lrcid & 0xFF00) >> 8
    if (lrcid & 0x00ff0000) == 0:
        t3 = 0xFF & ~t1
    else:
        t3 = 0xFF & ((lrcid & 0x00FF0000) >> 16)

    t3 = t3 | ((0xFF & lrcid) << 8)
    t3 = t3 << 8
    t3 = t3 | (0xFF & t1)
    t3 = t3 << 8
    if (lrcid & 0xFF000000) == 0:
        t3 = t3 | (0xFF & (~lrcid))
    else:
        te = t3 | (0xFF & (lrcid >> 24))

    t2 = 0
    j = length - 1
    while j >= 0:
        c = song[j]
        if c >= 0x80: c = c - 0x100
        t1 = int((c + t2) & 0xFFFFFFFF)
        t2 = int((t2 << (j % 2 + 4)) & 0xFFFFFFFF)
        t2 = int((t1 + t2) & 0xFFFFFFFF)
        j -= 1
    j = 0
    t1 = 0
    while j<= length - 1:
        c = song[j]
        if c > 128:c-=256
        t4 = int((c + t1) & 0xFFFFFFFF)
        t1 = int((t1 << (j % 2 + 3)) & 0xFFFFFFFF)
        t1 = int((t1 + t4) & 0xFFFFFFFF)
        j += 1
    print '1',t2,t3
    t5 = int(Conv(t2 ^ t3))
    print '2',t5
    t5 = int(Conv(t5 + (t1 | lrcid)))
    print '3',t5
    t5 = int(Conv(t5 * (t1 | t3)))
    print '4',t5
    t5 = int(Conv(t5 * (t2 ^ lrcid)))

    t6 = long(t5)
    if t6 > 2147483648:t5 = int(t6 - 4294967296)
    return str(t5)
    #return 'http://ttlrccnc.qianqian.com/dll/lyricsvr.dll?dl?Id='+str(lrcid)+'&Code='+str(t5)\
    #    +'&ci=545b5b56544d436111147132492b345316101c02111c6d5c252a265b534644141c464808425c5353011d01'

def Conv(i):
    r = long(i % 4294967296)
    if (i>=0 and r>2147483648):
        r -= 4294967296
    if (i<0 and r<2147483648):
        r += 4294967296
    return r

def GetQueryQQ(singer, title):
    result = []#查询结果
    s = singer.lower()
    t = title.lower()
    url = 'http://shopcgi.qqmusic.qq.com/fcgi-bin/shopsearch.fcg?value='+urllib.quote_plus(t.encode('gbk'))\
        +'&type=qry_song&out=json&page_no=1&page_record_num=5'
    socks = urllib.urlopen(url)
    print url
    js = socks.read()
    js = js[15:len(js)-2].decode('gbk')
    js = js.replace('",','","')
    js = js.replace(':','":')
    js = js.replace('{','{"')
    print js
    lrcs = json.loads(js)
    for lrc in lrcs['songlist']:
        #dat = lrc.items()
        result.append((lrc['singer_name'],lrc['song_name'],lrc['song_id']))
    return result

class Application(Frame):
    def createWidgets(self):
        self.FrameLeft1 = Frame(self)
        self.label1 = Label(self.FrameLeft1, text = 'Artist:')
        self.label1.pack(side=LEFT,padx = 5, pady = 2, anchor = NW)
        self.edtArtist = Entry(self.FrameLeft1)
        self.edtArtist.pack(side=LEFT,padx = 5, pady = 2, anchor = NW, expand = YES, fill = X)
        self.label2 = Label(self.FrameLeft1, text = 'Title:')
        self.label2.pack(side=LEFT,padx = 5, pady = 2, anchor = NW)
        self.edtTitle = Entry(self.FrameLeft1)
        self.edtTitle.pack(side=LEFT,padx = 5, pady = 2, anchor = NW, expand = YES, fill = X)
        self.FrameLeft1.pack(anchor = N,fill = X)

        self.FrameLeft2 = Frame(self)
        self.cnc = Radiobutton(self.FrameLeft2, text = '千千网通服务器')
        self.cnc.pack(side = LEFT, padx = 5, pady = 2, anchor = N)
        self.ctc = Radiobutton(self.FrameLeft2, text = '千千电信服务器')
        self.ctc.pack(side = LEFT, padx = 5, pady = 2, anchor = N)
        self.btnSearch = Button(self.FrameLeft2, text = u'开始搜索所选的服务器')
        self.btnSearch.pack(side = RIGHT, padx = 5, pady = 2, anchor = E)
        self.btnSearch['command'] = self.Search
        self.FrameLeft2.pack(anchor = N,fill = X)

        self.lst = Listbox(self, height = 8)
        self.lst.pack(anchor = N, fill = X, padx = 5, pady = 2)
        self.lst.bind('<Double-Button-1>',self.GetLyric)

        self.FrameRight = Frame(self)
        self.scrbar = Scrollbar(self.FrameRight)
        self.scrbar.pack(side = RIGHT, pady = 2, anchor = N, fill = Y)
        self.edtLyric = Text(self.FrameRight, height = 24, yscrollcommand = self.scrbar.set)
        self.scrbar['command'] = self.edtLyric.yview
        self.edtLyric.pack(pady = 2, fill = BOTH, anchor = N)
        self.FrameRight.pack(anchor = S, fill = Y, expand = YES, padx = 5)

        self.label3 = Label(self, text = u'保存到文件:')
        self.label3.pack(side = LEFT, anchor = S, padx = 5, pady = 6)
        self.edtName = Entry(self)
        self.edtName.pack(side = LEFT, anchor = S, padx = 5, pady = 6, fill=X, expand = YES)
        self.btnSave = Button(self, text = u'保存')
        self.btnSave.pack(side = LEFT, anchor = S, padx = 5, pady = 6)
        
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.pack(expand = YES, fill = BOTH)
        self.master.title('TTPlayer Lyric Fetch')
        self.master.geometry("400x595")
        self.master.minsize(400,595)
        self.master.maxsize(600,595)
        self.createWidgets()

    def Search(self):
        art = self.edtArtist.get()
        title = self.edtTitle.get()
        self.res = GetQuery(art, title)
        if len(self.res)==0:print 'Not Found'
        self.lst.delete(0,END)
        for item in self.res:
            self.lst.insert(END, item[2] +' - '+ item[0]+' - '+item[1])

    '''def Search(self):
        art = self.edtArtist.get()
        title = self.edtTitle.get()
        self.res = GetQueryQQ(art, title)
        if len(self.res)==0:print 'Not Found'
        self.lst.delete(0,END)
        for item in self.res:
            self.lst.insert(END, item[2] +' - '+ item[0]+' - '+item[1])'''

    def GetLyric(self,event):
        i = self.lst.curselection()
        item = self.res[int(i[0])]
        url = GetCode(item[0],item[1],int(item[2]))
        print url,item
        text = urllib.urlopen(url).read()
        self.edtLyric.insert(1.0, text)

    '''def GetLyric(self,event):
        i = self.lst.curselection()
        item = self.res[int(i[0])]
        url = 'http://music.qq.com/miniportal/static/lyric/'+item[2][4:]+'/'+item[2]+'.xml'
        print url,item
        text = urllib.urlopen(url).read()
        text = text.decode('gbk')
        self.edtLyric.delete(1.0, END)
        if 'html' in text:
            self.edtLyric.insert(1.0, '未找到')
        else:
            self.edtLyric.insert(1.0, text)'''
        
root = Tk()
app = Application(master = root)
app.mainloop()
root.destroy()     
