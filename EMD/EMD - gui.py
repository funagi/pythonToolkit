#encoding=utf-8
import Image,wx,math
#import ImageDraw
from vector import *
import DrawElectDio,DrawElectPoint
        
        
class Gui(wx.Frame):
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self, parent, id, title,pos=(150, 150), size=(800, 650))
        tbook = wx.Toolbook(self, -1, style = wx.BK_LEFT,size=(800,650))
        #图片列表
        il = wx.ImageList(64, 64)
        for x in range(2):
            bmp = wx.Bitmap('icon_%d.png'%x,type=wx.BITMAP_TYPE_PNG)
            il.Add(bmp)
        tbook.AssignImageList(il)
        tbook.AddPage(DrawElectDio.DrawElectDio(tbook,-1,(800, 500)),u'电偶极子',imageId = 0)
        tbook.AddPage(DrawElectPoint.DrawElectPoint(tbook,-1,(800, 500)),u'点电荷',imageId = 1)

class Main(wx.App):
    def OnInit(self):
        frame = Gui(None, -1, u'EM Display')
        self.SetTopWindow(frame)
        frame.Show(True)
        return True

app=Main(0)#redirect=True，重定向输出
app.MainLoop()
