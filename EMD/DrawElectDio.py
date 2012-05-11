import Image,colorsys,math,wx
#import ImageDraw as draw
from vector import *

class DrawElectDio(wx.Panel):
    def __init__(self,parent,id,Size):
        wx.Panel.__init__(self, parent, id, size=Size)
        self.Size = (400,400)
        s = self.Size
        s = min([s[0],s[1]])
        self.img = wx.StaticBitmap(self, -1, pos=(5,35), size=(400,400))
        b = wx.Button(self, -1, u'计算', pos=(5,5))
        self.dio = wx.TextCtrl(self,-1,pos = (105,5))
        self.Bind(wx.EVT_BUTTON,self.Start,b)

    def Start(self,event):
        t = self.dio.GetLineText(0)
        i = Image.new('RGB',(600,600))
        p = vector(int(t[:t.index(',')]),int(t[t.index(',')+1:t.rindex(',')]),int(t[t.rindex(',')+1:]))
        ma = 1
        mi = 0
        phi = [[0 for b in range(-300,300)] for b in range(-300,300)]
        for x in range(-300,300):
            for y in range(-300,300):
                if x==0 and y==0:continue
                pr = p * vector(x,y,0)
                phi[x+300][y+300] = pr/((math.sqrt(x*x+y*y))**3)*10000
                if phi[x+300][y+300]>ma:ma = phi[x+300][y+300]
                if phi[x+300][y+300]<mi:mi = phi[x+300][y+300]
        print ma,mi
        for x in range(0,600):
            for y in range(0,600):
                c = colorsys.hsv_to_rgb(phi[x][y]%360,1,1)
                c = (int(c[0]*255),int(c[1]*255),int(c[2]*255))
                #sprint x,y,c
                i.putpixel((x,y),c)
        i.save('1.jpg')
        self.img.SetBitmap(wx.Bitmap('1.jpg',type=wx.BITMAP_TYPE_JPEG))
