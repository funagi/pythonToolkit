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
        self.edtText.bind('<Key>',self.Search)
        
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.pack(expand = YES, fill = BOTH)
        self.master.title('Paper Index Local Version')
        self.master.geometry("600x400")
        self.createWidgets()
        #载入数据库
        self.db = sqlite3.connect(u'paper.sqlite')

    def Search(self,event):
        if event.char in [' ','\b']:return
        key = event.widget.get()+event.char
        
        if key == u'':
            return False
        else:
            keylist = key.split(' ')
            keyliststring = '%" and Fullinfo like "%'.join(keylist)
            self.lst.delete(0,END)
            command = 'select * from paper where Fullinfo like "%' + keyliststring + '%"'
            #print command
            c = self.db.cursor()
            c.execute(command)
            for item in c:
                print item
                self.lst.insert(END, item[0])
            c.close()
            

root = Tk()
app = Application(master = root)
app.mainloop()
