import Image,colorsys,math,wx
from vector import *

class DrawElectPoint(wx.Panel):
    def __init__(self,parent,id,Size):
        wx.Panel.__init__(self, parent, id, size=Size)
        self.Size = (400,400)
        s = self.Size
        s = min([s[0],s[1]])
        self.img = wx.StaticBitmap(self, -1, pos=(5,35), size=(400,400))
        b = wx.Button(self, -1, u'计算', pos=(5,5))
        self.ba = wx.Button(self, -1, u'添加', pos=(205,5))
        self.dio = wx.TextCtrl(self,-1,pos = (105,5))
        self.Bind(wx.EVT_BUTTON,self.Start,b)
        self.Bind(wx.EVT_BUTTON,self.Add,self.ba)
        self.points=[]

    def Add(self,event):
        t = self.dio.GetLineText(0)
        lst = t.split(',')
        p = vector(int(lst[0]),int(lst[1]),int(lst[2]))
        self.points.append((p,float(lst[3])))

    def Start(self,event):
        
        i = Image.new('RGB',(600,600))
        ma = 1
        mi = 0
        phi = [[0.0 for b in range(-300,300)] for b in range(-300,300)]
        for x in range(-300,300):
            for y in range(-300,300):
                for p in self.points:
                    if x==p[0][0] and y==p[0][1]:continue
                    phi[x+300][y+300] += p[1]/((vector(x,y,0)-p[0]).length())*10000
                if phi[x+300][y+300]>ma:ma = phi[x+300][y+300]
                if phi[x+300][y+300]<mi:mi = phi[x+300][y+300]
        for x in range(0,600):
            for y in range(0,600):
                c = colorsys.hsv_to_rgb(float(phi[x][y]-mi)/(ma-mi)*100.0,1,1)
                c = (int(c[0]*255),int(c[1]*255),int(c[2]*255))
                i.putpixel((x,y),c)
        i.save('1.jpg')
        self.img.SetBitmap(wx.Bitmap('1.jpg',type=wx.BITMAP_TYPE_JPEG))
