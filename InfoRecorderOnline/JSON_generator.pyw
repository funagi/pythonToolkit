# encoding: utf-8
import json
from wx import Frame,App,Panel,GridBagSizer,TextCtrl,BoxSizer,Button,RadioButton
from wx import DEFAULT_FRAME_STYLE,TE_MULTILINE,RESIZE_BORDER,MAXIMIZE_BOX,EVT_BUTTON
import  wx.lib.anchors as anchors

class Query_Frame(Frame):
    def __init__(self,parent,id,title):
        Frame.__init__(self, parent, id, title,pos=(150, 150), size=(510, 440),
                          style=DEFAULT_FRAME_STYLE & ~(RESIZE_BORDER | MAXIMIZE_BOX))
        p = self.panel = Panel(self, -1, size=(520, 455))
        p.SetAutoLayout(True)
        #Place controls
        self.textin = TextCtrl(p, -1, style=TE_MULTILINE, size=(500,200), pos=(10,10))

        self.btnStart = Button(p, -1, u"Convertヽ（゜д゜）ノ", pos=(80,215))
        self.btnStart.Bind(EVT_BUTTON, self.Convert)
        self.optSeiyuu = RadioButton(p, -1, "Seiyuu", pos=(260,220))
        self.optSeiyuu.SetValue(True)
        self.optMemo = RadioButton(p, -1, "Memo", pos=(360,220))

        self.textout = TextCtrl(p, -1, style=TE_MULTILINE, size=(500,200), pos=(10,245))

        self.SetClientSize(p.GetSize())



    def Convert(self,event):
        textin = self.textin.GetValue()
        data = []

        #print self.optSeiyuu.GetValue()
        if self.optSeiyuu.GetValue():
            for text in textin.split('\n'):
                array = text.split(',')
                if len(array)==4:
                    data.append({'chara':array[0],'name':array[1],'alias':array[2],'id':array[3]})
        
        elif self.optMemo.GetValue():
            for text in textin.split('\n'):
                array = text.split(',')
                if len(array)==2:
                    data.append({'label':array[0],'link':array[1]})
         
        textout = json.dumps(data)
        self.textout.SetValue(textout)


class Query_Gui(App):
    def OnInit(self):
        frame = Query_Frame(None, -1, u"InfoRecorder JSON Generator ヽ（´ー｀）ノ")
        self.SetTopWindow(frame)
        frame.Show(True)
        return True
        
        
app=Query_Gui(0)#redirect=True)#Redirect output
app.MainLoop()
