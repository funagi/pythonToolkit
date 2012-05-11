#encoding=utf-8
import wx,os

class FileDropTarget(wx.FileDropTarget):
    def __init__(self,window):
        wx.FileDropTarget.__init__(self)
        self.window=window

    def OnDropFiles(self,x,y,filenames):
        sourcefile = open(filenames[0],'rb')
        a=sourcefile.read()
        self.window.SetValue('')
        self.window.WriteText(a.encode('base64'))
        sourcefile.close()
                
class Query_Frame(wx.Frame):
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self, parent, id, title,pos=(150, 150), size=(625, 422))
        #生成Panel
        self.panel=wx.Panel(self,-1)
        #放置控件
        self.edt = wx.TextCtrl(self.panel,-1,pos=(10,10),size=(595,332),style=wx.TE_MULTILINE)
        self.btnSave = wx.Button(self.panel,-1,'&Save as text')
        self.btnExit = wx.Button(self.panel,-1,'E&xit program')
        self.tip = wx.StaticText(self.panel,-1,'Drag and drop file to convert')
        tipfont = wx.Font(20,wx.SCRIPT,wx.NORMAL,wx.NORMAL)
        tipfont.MakeBold()
        self.tip.SetBackgroundColour('white')
        self.tip.SetForegroundColour('grey')
        self.tip.SetFont(tipfont)
        #绑定事件
        self.Bind(wx.EVT_SIZE,self.OnSize,self)
        self.btnExit.Bind(wx.EVT_BUTTON,self.OnClose)
        DropTarget = FileDropTarget(self.edt)
        self.edt.SetDropTarget(DropTarget)
        self.btnSave.Bind(wx.EVT_BUTTON,self.Save)

    def OnClose(self,evt):
        self.Close(False)
        
    def OnSize(self,evt):#缩放窗口
        self.panel.Size=self.Size
        self.edt.Size=(self.Size[0]-30,self.Size[1]-90)
        self.btnSave.Position=(self.Size[0]-195,self.Size[1]-75)
        self.btnExit.Position=(self.btnSave.Position[0]+85,self.btnSave.Position[1])
        self.tip.Position=(self.edt.Size[0]/2-200,self.edt.Size[1]/2)

    def Save(self,evt):
        wcard = 'Text File (*.txt)|*.txt|'\
                'All files (*.*)|*.*'
        dlgsave = wx.FileDialog(
            self,message = 'Save Base64 text as ...', defaultDir = os.getcwd(),
            defaultFile = 'base64.txt', wildcard = wcard, style = wx.SAVE
            )
        if dlgsave.ShowModal() == wx.ID_OK:
            path = dlgsave.GetPath()
            f = file(path, 'w')
            f.write(self.edt.GetLineText())
            f.close()
        dlgsave.Destory()

class Query_Gui(wx.App):
    def OnInit(self):
        frame = Query_Frame(None, -1, u"Base64 String Converter")
        self.SetTopWindow(frame)
        frame.Show(True)
        return True
        
        
app=Query_Gui(0)#redirect=True
app.MainLoop()
