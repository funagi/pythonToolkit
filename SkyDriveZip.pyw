#encoding=utf-8
import wx,zipfile,os

class FileDropTarget(wx.FileDropTarget):
    def __init__(self,window):
        wx.FileDropTarget.__init__(self)
        self.window=window

    def OnDropFiles(self,x,y,filenames):
        #self.window.SetValue(filenames[0])
        for filename in filenames:
            f = zipfile.ZipFile(filename)
            namelist = [[],[]]
            try:
                info = f.open(ur'Encoding Errors.txt','r')
                originlist = f.namelist()
                f.getinfo(u'Encoding Errors.txt').filename='1.txt'
                for line in info.readlines():
                    if (line.find(' -> ')!=-1) and (line.find('Original File Name  ->  New File Name')==-1):
                        namelist[0].append(line[:line.index(' -> ')])
                        namelist[1].append(line[line.index(' -> ')+4:].replace('\r\r\n',''))
                self.window.WriteText(str(originlist))
                newfile = zipfile.ZipFile(filename[:len(filename)-4]+'.renamed.zip','a')
                for name in originlist:
                    if name == 'Encoding Errors.txt':continue
                    f.extract(name,'temp')
                    if name in namelist[1]:
                        i = namelist[1].index(name)
                        newfile.write('temp\\'+namelist[1][i],namelist[0][i].decode('utf-8').encode('gbk'))
                    else:
                        newfile.write('temp\\'+name,name)
                    os.remove('temp\\'+name)
                os.rmdir('temp')
                f.close()
                newfile.close()
                self.window.WriteText(filename+': Parsed successfully.\n')
            except KeyError:
                self.window.WriteText(filename+': This Zip file does not require renaming.\n')
            except zipfile.BadZipfile:
                self.window.WriteText(filename+': Not ZIP file.\n')

class Query_Frame(wx.Frame):
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self, parent, id, title,pos=(150, 150), size=(625, 422))
        #生成Panel
        self.panel=wx.Panel(self,-1)
        #放置控件
        self.edt = wx.TextCtrl(self.panel,-1,pos=(10,10),size=(595,332),style=wx.TE_MULTILINE)
        self.btnSave = wx.Button(self.panel,-1,'&Save as text')
        self.btnExit = wx.Button(self.panel,-1,'E&xit program')
        self.tip = wx.StaticText(self.panel,-1,'Drag and drop file to rename')
        tipfont = wx.Font(20,wx.SCRIPT,wx.NORMAL,wx.NORMAL)
        tipfont.MakeBold()
        self.tip.SetBackgroundColour('white')
        self.tip.SetForegroundColour('grey')
        self.tip.SetFont(tipfont)
        #绑定事件
        self.Bind(wx.EVT_SIZE,self.OnSize,self)
        self.btnExit.Bind(wx.EVT_BUTTON,self.Close,self)
        DropTarget = FileDropTarget(self.edt)
        self.edt.SetDropTarget(DropTarget)


    def OnSize(self,evt):#缩放窗口
        self.panel.Size=self.Size
        self.edt.Size=(self.Size[0]-30,self.Size[1]-90)
        self.btnSave.Position=(self.Size[0]-195,self.Size[1]-75)
        self.btnExit.Position=(self.btnSave.Position[0]+85,self.btnSave.Position[1])
        self.tip.Position=(self.edt.Size[0]/2-190,self.edt.Size[1]/2)


        

class Query_Gui(wx.App):
    def OnInit(self):
        frame = Query_Frame(None, -1, u"SkyDrive Zip File Renamer")
        self.SetTopWindow(frame)
        frame.Show(True)
        return True
        
        
app=Query_Gui(redirect=True)#redirect=True
app.MainLoop()
