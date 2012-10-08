# coding = utf-8
from Tkinter import *
def test(t):
    if len(t)<9:
        t = t+'0'*(9-len(t))
    r=[['1','2','3'],['4','5','6'],['7','8','9'],['1','4','7'],['2','5','8'],['3','6','9'],['1','5','9'],['3','5','7']]
    a = [t[0],t[2],t[4],t[6],t[8]]
    b = [t[1],t[3],t[5],t[7]]
    a.sort()
    b.sort()
    result = '0'
    for p in r:
        if a.count(p[0]) and a.count(p[1]) and a.count(p[2]):
            result = '1'
        if b.count(p[0]) and b.count(p[1]) and b.count(p[2]):
            result = '2'
    return result
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


    def Guess(self,srgs=[range(1,10)]*9):
        r={'0':0,'1':0,'2':0}
        for s1 in srgs[0]: #s1
            for s2 in srgs[1]: #s2
                if s2!=s1:
                    for s3 in srgs[2]: #s3
                        if s3!=s1 and s3!=s2:
                            for s4 in srgs[3]: #s4
                                if s4!=s3 and s4!=s2 and s4!=s1:
                                    for s5 in srgs[4]: #s5
                                        if s5!=s4 and s5!=s3 and s5!=s2 and s5!=s1:
                                            res = test(str(s1*10000+s2*1000+s3*100+s4*10+s5))
                                            if res!='0':
                                                r[res]+=1
                                                continue
                                            else:
                                                for s6 in srgs[5]: #s6
                                                    if s6!=s5 and s6!=s4 and s6!=s3 and s6!=s2 and s6!=s1:
                                                        res = test(str(s1*100000+s2*10000+s3*1000+s4*100+s5*10+s6))
                                                        if res!='0':
                                                            r[res]+=1
                                                            continue
                                                        else:
                                                            for s7 in srgs[6]: #s7
                                                                if s7!=s6 and s7!=s5 and s7!=s4 and s7!=s3 and s7!=s2 and s7!=s1:
                                                                    res = test(str(s1*1000000+s2*100000+s3*10000+s4*1000+s5*100+s6*10+s7))
                                                                    if res!='0':
                                                                        r[res]+=1
                                                                        continue
                                                                    else:
                                                                        for s8 in srgs[7]: #s8
                                                                            if s8!=s7 and s8!=s6 and s8!=s5 and s8!=s4 and s8!=s3 and s8!=s2 and s8!=s1:
                                                                                res = test(str(s1*10000000+s2*1000000+s3*100000+s4*10000+s5*1000+s6*100+s7*10+s8))
                                                                                if res!='0':
                                                                                    r[res]+=1
                                                                                    continue
                                                                            else:
                                                                                for s9 in srgs[8]:
                                                                                    if s9!=s8 and s9!=s7 and s9!=s6 and s9!=s5 and s9!=s4 and s9!=s3 and s9!=s2 and s9!=s1:
                                                                                        res = test(str(s1*100000000+s2*10000000+s3*1000000+s4*100000+s5*10000+s6*1000+s7*100+s8*10+s9))
                                                                                        if res!='0':
                                                                                            r[res]+=1
                                                                                            continue
                                                                                            #t+=1
                                                                                        else:
                                                                                            r['0']+=1
                                                                                            #t+=1
        r['t']=r['0']+r['1']+r['2']
        return r

    
    def Search(self):
        #print self
        key = self.key.get()
        if key == u'':
            return False
        else:
            self.lst.delete(0,END)
            
            for x in range(1,10):
                if str(x) not in key:
                    r = self.Guess([[int(n)] for n in key]+[[x]]+[range(1,10)]*(8-len(key)))
                    if r['t']!=0:
                        self.lst.insert(END, '  '.join([str(x),str(float(r['1'])/(r['t'])),str(float(r['2'])/(r['t']))]))
            
    def Search2(self,event):
        print self
        self.Search()
        
root = Tk()
app = Application(master = root)
app.mainloop()
root.destroy()
