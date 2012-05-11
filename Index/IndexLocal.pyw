# coding = utf-8
from Tkinter import *
import sqlite3

def Path(info):
    if(info[3]==''):
        return 'ftp://'+info[1]+':'+str(info[2])
    else:
        return 'ftp://'+info[3]+':'+info[4]+'@'+info[1]+':'+str(info[2])
    
class Application(Frame):
    def createWidgets(self):
        self.label = Label(self, text = '关键字:')
        self.label.pack(side=LEFT,padx = 5, pady = 5, anchor = NW)
        self.edtText = Entry(self)
        self.edtText.pack(side=LEFT,padx = 5, pady = 5, anchor = NW, expand = YES, fill = X)
        self.btnSearch = Button(self)
        self.btnSearch['text'] = u'  搜索(&S)  '
        self.btnSearch['font'] = u'宋体 8'
        self.btnSearch['command'] = self.Search
        self.btnSearch.pack(side = RIGHT, padx = 5, pady = 5, anchor = NE)
        self.lst = Listbox(self)
        self.lst.pack(side = BOTTOM, padx = 5,pady = 5, fill = BOTH, anchor = SW, expand = YES, before = self.label)
        self.key = StringVar()
        self.key.set('')
        self.edtText['textvariable'] = self.key
        self.edtText.bind('<Key-Return>',self.Search2)
        
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.pack(expand = YES, fill = BOTH)
        self.master.title('Index Local Version')
        self.master.geometry("600x400")
        self.createWidgets()
        #载入数据库
        self.db = sqlite3.connect(u'IndexLocal.db3')
        #self.db.text_factory = str
        self.ftp_list = []
        c = self.db.cursor()
        c.execute('select * from db_ftp')
        self.ftp_list = c.fetchall()
        c.close()

    def Search(self):
        #print self
        key = self.key.get()
        if key == u'':
            return False
        else:
            self.lst.delete(0,END)
            for ftp in self.ftp_list:
                c = self.db.cursor()
                print ftp,ftp[0]
                c.execute("SELECT COUNT(*) FROM sqlite_master where type='table' and name='"+ftp[0]+"'")
                exist = c.fetchall()
                print exist
                if (0,) in exist: continue
                print 'select * from '+ftp[0]+" where path like '%"+key+"%'"
                c.execute('select * from '+ftp[0]+" where path like '%"+key+"%'")
                for item in c:
                    self.lst.insert(END, Path(ftp)+item[1][1:])
                c.close()
            print 'yes'
    def Search2(self,event):
        print self
        self.Search()
        
root = Tk()
app = Application(master = root)
app.mainloop()
root.destroy()
