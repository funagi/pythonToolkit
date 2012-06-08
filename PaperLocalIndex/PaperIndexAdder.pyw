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
        self.columnconfigure(0, pad=3)
        self.columnconfigure(1, pad=3, weight=1)
        self.rowconfigure(0, pad=3)
        self.rowconfigure(1, pad=3)
        self.rowconfigure(2, pad=3)
        self.rowconfigure(3, pad=3)
        self.rowconfigure(4, pad=3)
        self.rowconfigure(5, pad=3)
        self.rowconfigure(6, pad=3)
        self.rowconfigure(7, pad=3)
        self.rowconfigure(8, pad=3)

        self.rowconfigure(9, pad=3)
        self.rowconfigure(10, pad=3)
        self.rowconfigure(11, pad=3)
        self.rowconfigure(12, pad=3)
        
        self.i=0
        self.label = Label(self, text = 'Title:')
        self.label.grid(row=self.i, column=0, sticky=W)
        self.edtTitle = Entry(self)
        self.edtTitle.grid(row=self.i, column=1, sticky=W+E)
        self.i+=1
        
        self.label = Label(self, text = 'Year:')
        self.label.grid(row=self.i, column=0, sticky=W)
        self.edtYear = Entry(self)
        self.edtYear.grid(row=self.i, column=1, sticky=W+E)
        self.i+=1
        
        self.label = Label(self, text = 'Magazine:')
        self.label.grid(row=self.i, column=0, sticky=W)
        self.edtMagazine = Entry(self)
        self.edtMagazine.grid(row=self.i, column=1, sticky=W+E)
        self.i+=1
        
        self.label = Label(self, text = 'Keywords:')
        self.label.grid(row=self.i, column=0, sticky=W)
        self.edtKeywords = Entry(self)
        self.edtKeywords.grid(row=self.i, column=1, sticky=W+E)
        self.i+=1
        
        self.label = Label(self, text = 'Author:')
        self.label.grid(row=self.i, column=0, sticky=W)
        self.edtAuthor = Entry(self)
        self.edtAuthor.grid(row=self.i, column=1, sticky=W+E)
        self.i+=1
        
        self.label = Label(self, text = 'File Path:')
        self.label.grid(row=self.i, column=0, sticky=W)
        self.edtPath = Entry(self)
        self.edtPath.grid(row=self.i, column=1, sticky=W+E)
        self.i+=1
        
        self.btnStart = Button(self)
        self.btnStart['text'] = u'  Insert!  '
        #self.btnStart['font'] = u'宋体 8'
        self.btnStart['command'] = self.Add
        self.btnStart.grid(row=self.i, column=0, columnspan=2)
        self.i+=1

        
        
        self.pack()
        
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.pack(expand = YES, fill = BOTH)
        self.master.title('Paper Index Local Version Adder')
        self.createWidgets()
        self.master.geometry("600x400")
        #载入数据库
        self.db = sqlite3.connect(u'paper.sqlite')


    def Add(self):
        # gather information
        title = self.edtTitle.get()
        year = self.edtYear.get()
        magazine = self.edtMagazine.get()
        keywords = self.edtKeywords.get()
        author = self.edtAuthor.get()
        path = self.edtPath.get()
        full = '%s %s %s %s %s %s' % (title,year,magazine,keywords,author,path)
        # add entry
        c = self.db.cursor()
        c.execute('INSERT INTO paper VALUES (?,?,?,?,?,null,?,?)',
                  (title,year,magazine,keywords,author,path,full))
        c.close()
        self.db.commit()
        
    def Search2(self,event):
        print self
        self.Search()
        
root = Tk()
app = Application(master = root)
app.mainloop()
root.destroy()
