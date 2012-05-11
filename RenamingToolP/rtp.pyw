#encoding=utf-8
import wx,os,re,base64,zlib,StringIO
import  wx.lib.anchors as anchors

class Query_Frame(wx.Frame):
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self, parent, id, title,pos=(150, 150), size=(800, 500))
        self.SetMinSize((800,500))
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(self.DecodeBase64(icoMain,0))
        self.SetIcon(icon)
        
        #-------------------------------生成Panel-------------------------------
        self.panel=wx.Panel(self,-1,style=wx.TAB_TRAVERSAL | wx.CLIP_CHILDREN | wx.FULL_REPAINT_ON_RESIZE)
        self.panel.Size=(800,500)
        self.panel.SetAutoLayout(True)
        
        #--------------------------------控件坐标-------------------------------
        x=[5,570]
        y=[5,31]
        
        #--------------------------------放置控件-------------------------------
        self.txtDir = wx.StaticText(self.panel,-1,u'目标目录：',(x[0],y[0]+3))
        self.txtDir.BackgroundColour=(245,245,245,255)
        self.edtDir = wx.TextCtrl(self.panel,-1,u'',(x[0]+65,y[0]),(600,21),wx.TE_PROCESS_ENTER)
        self.edtDir.SetConstraints(anchors.LayoutAnchors(self.edtDir, 1, 1, 1, 0))
        self.btnBrowse = wx.Button(self.panel,-1,u'浏览(&B)',(675,y[0]))
        self.btnBrowse.SetConstraints(anchors.LayoutAnchors(self.btnBrowse,0,1,1,0))
        self.btnRefresh = wx.Button(self.panel,-1,u'',(755,y[0]),(23,23))
        self.btnRefresh.SetBitmap(self.DecodeBase64(icoRefresh,0))
        self.btnRefresh.SetConstraints(anchors.LayoutAnchors(self.btnRefresh,0,1,1,0))
        self.mlist = wx.ListBox(self.panel,-1,(x[0],36),(575,370),style=wx.LB_SINGLE)
        self.mlist.SetConstraints(anchors.LayoutAnchors(self.mlist, 1, 1, 1, 1))

        self.boxReplace = wx.StaticBox(self.panel,-1,u'批量替换',(x[1]+15,y[1]),(195,170))
        self.boxReplace.BackgroundColour=(245,245,245,255)
        self.boxReplace.SetConstraints(anchors.LayoutAnchors(self.boxReplace, 0, 1, 1, 0))
        x.append(self.boxReplace.Position[0]+5)
        y.append(self.boxReplace.Position[1]+20)
        self.edtText1 = wx.TextCtrl(self.panel,-1,u'',(x[2],y[2]),(185,21))
        self.edtText1.SetConstraints(anchors.LayoutAnchors(self.edtText1,0,1,1,0))
        self.edtText2 = wx.TextCtrl(self.panel,-1,u'',(x[2],y[2]+26),(185,21))
        self.edtText2.SetConstraints(anchors.LayoutAnchors(self.edtText2,0,1,1,0))
        self.btnReplace = wx.Button(self.panel,-1,u'普通替换',(x[2],y[2]+52),(90,90),wx.BU_BOTTOM)
        self.btnReplace.SetBitmap(self.DecodeBase64(icoReplace,0),wx.TOP)
        self.btnReplace.SetConstraints(anchors.LayoutAnchors(self.btnReplace,0,1,1,0))
        self.btnPrefix = wx.Button(self.panel,-1,u'添加前缀',(x[2]+95,y[2]+52),(90,90),wx.BU_BOTTOM)
        self.btnPrefix.SetBitmap(self.DecodeBase64(icoPrefix,0),wx.TOP)
        self.btnPrefix.SetConstraints(anchors.LayoutAnchors(self.btnPrefix,0,1,1,0))

        self.boxQuick = wx.StaticBox(self.panel,-1,u'快捷操作',(x[1]+15,y[1]+self.boxReplace.Size[1]+5),(195,121))
        self.boxQuick.BackgroundColour=(245,245,245,255)
        self.boxQuick.SetConstraints(anchors.LayoutAnchors(self.boxQuick, 0, 1, 1, 0))
        self.btnCRC = wx.Button(self.panel,-1,u'消除CRC',(x[2]+55,y[1]+self.boxReplace.Size[1]+20))
        self.btnCRC.SetConstraints(anchors.LayoutAnchors(self.btnCRC, 0, 1, 1, 0))
        self.edtRegex = wx.TextCtrl(self.panel,-1,u'',(x[2],y[1]+self.boxReplace.Size[1]+46),(185,21))
        self.edtRegex.SetConstraints(anchors.LayoutAnchors(self.edtRegex, 0, 1, 1, 0))
        self.edtText3 = wx.TextCtrl(self.panel,-1,u'',(x[2],y[1]+self.boxReplace.Size[1]+72),(185,21))
        self.edtText3.SetConstraints(anchors.LayoutAnchors(self.edtText3,0,1,1,0))
        self.btnRegex = wx.Button(self.panel,-1,u'正则替换',(x[2]+55,y[1]+self.boxReplace.Size[1]+98))
        self.btnRegex.SetConstraints(anchors.LayoutAnchors(self.btnRegex,0,1,1,0))

        self.btnUndo = wx.Button(self.panel,-1,u'撤销操作',(x[1]+15,self.boxQuick.Position[1]+self.boxQuick.Size[1]+5),(90,23))
        self.btnUndo.SetBitmap(self.DecodeBase64(icoUndo,0))
        self.btnUndo.SetConstraints(anchors.LayoutAnchors(self.btnUndo,0,1,1,0))
        self.btnUndo.Disable()
        self.btnClear = wx.Button(self.panel,-1,u'清空列表',(x[1]+120,self.boxQuick.Position[1]+self.boxQuick.Size[1]+5),(90,23))
        self.btnClear.SetBitmap(self.DecodeBase64(icoDelete,0))
        self.btnClear.SetConstraints(anchors.LayoutAnchors(self.btnClear,0,1,1,0))

        bigfont = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        bigfont.SetPixelSize((8,9))
        bigfont.SetPointSize(11)
        self.btnStart = wx.Button(self.panel,-1,u'开始操作',(275,416),(130,33),style=wx.BORDER_NONE)
        self.btnStart.SetBitmap(self.DecodeBase64(icoStart,23))
        self.btnStart.SetFont(bigfont)
        self.btnStart.SetConstraints(anchors.LayoutAnchors(self.btnStart,0,0,0,1))
        self.btnExit = wx.Button(self.panel,-1,u'退出程序',(415,416),(130,33),style=wx.BORDER_NONE)
        self.btnExit.SetBitmap(self.DecodeBase64(icoExit,23))
        self.btnExit.SetFont(bigfont)
        self.btnExit.SetConstraints(anchors.LayoutAnchors(self.btnExit,0,0,0,1))
        
        #--------------------------------绑定事件-------------------------------
        self.Bind(wx.EVT_SIZE,self.OnSize,self)
        self.Bind(wx.EVT_BUTTON,self.OnBrowse,self.btnBrowse)
        self.Bind(wx.EVT_BUTTON,self.OnRefresh,self.btnRefresh)
        self.Bind(wx.EVT_BUTTON,self.OnReplace,self.btnReplace)
        self.Bind(wx.EVT_BUTTON,self.OnPrefix,self.btnPrefix)
        self.Bind(wx.EVT_BUTTON,self.OnClear,self.btnClear)
        self.Bind(wx.EVT_BUTTON,self.OnUndo,self.btnUndo)
        self.Bind(wx.EVT_BUTTON,self.OnCRC,self.btnCRC)
        self.Bind(wx.EVT_TEXT_ENTER,self.OnBrowseText,self.edtDir)
        self.Bind(wx.EVT_BUTTON,self.OnRegex,self.btnRegex)
        self.Bind(wx.EVT_BUTTON,self.OnStart,self.btnStart)
        self.Bind(wx.EVT_BUTTON,self.OnExit,self.btnExit)
        
        #--------------------------------全局变量-------------------------------
        self.path = u''#路径
        self.stack = []#堆栈
        self.original = []#原始文件名

#-------------------------------BASE64文件解码----------------------------------
    def DecodeBase64(self,instr,size):
        data = zlib.decompress(base64.decodestring(instr.replace('\n','')))
        fp = StringIO.StringIO(data)
        if size>0:
            return wx.ImageFromStream(fp).Scale(size,size).ConvertToBitmap()
        else:
            return wx.ImageFromStream(fp).ConvertToBitmap()
    
#--------------------------------缩放窗口---------------------------------------        
    def OnSize(self,evt):
        self.panel.Size=self.Size

#-------------------------------浏览文件夹--------------------------------------
    def OnBrowse(self,event):
        try:
            self.mlist.Clear()
            dlg = wx.DirDialog(self,u'请选择目标文件夹：',style=wx.DD_DIR_MUST_EXIST)
            if dlg.ShowModal()==wx.ID_OK:
                self.path = dlg.GetPath()               
            dlg.Destroy()
            self.original = os.listdir(self.path)
            self.mlist.InsertItems(self.original,0)
            self.edtDir.SetValue(self.path)
        except WindowsError:
            print 'WindowsError'

#-----------------------------从文本框浏览文件夹---------------------------------
    def OnBrowseText(self,event):
        try:
            self.mlist.Clear()
            text = self.edtDir.GetLineText(0)
            self.original = os.listdir(text)
            self.mlist.InsertItems(self.original,0)
        except WindowsError as err:#(errno,errstr):
            if err.winerror==3:
                wx.MessageBox(u'找不到文件夹: '+text,u'文件系统错误',wx.OK|wx.ICON_ERROR)
            elif err.winerror==5:
                wx.MessageBox(u'拒绝访问: '+text,u'文件系统错误',wx.OK|wx.ICON_ERROR)
            else:
                wx.MessageBox(u'文件系统错误\n代码: '+err.winerror+u'\n位置: '+text,u'文件系统错误',wx.OK|wx.ICON_ERROR)
        
#--------------------------------刷新列表---------------------------------------
    def OnRefresh(self,event):
        try:
            if self.path==u'':return
            self.mlist.Clear()
            self.mlist.InsertItems(os.listdir(self.path),0)
            self.edtDir.SetValue(self.path)
        except WindowsError:
            print 'WindowsError'

#--------------------------------普通替换---------------------------------------
    def OnReplace(self,event):
        count = self.mlist.GetCount()
        if count==0:return
        list = []
        for i in range(0,count):
            txtA = self.edtText1.GetLineText(0)
            txtB = self.edtText2.GetLineText(0)
            item = self.mlist.GetString(i)
            list.append(item)
            item = item.replace(txtA,txtB)
            self.mlist.SetString(i,item)
        self.stack.append(list)   #push last into stack
        self.btnUndo.Enable()

#----------------------------------前缀-----------------------------------------
    def OnPrefix(self,event):
        count = self.mlist.GetCount()
        if count==0:return
        list = []
        for i in range(0,count):
            txtA = self.edtText1.GetLineText(0)
            item = self.mlist.GetString(i)
            list.append(item)
            item = txtA + item
            self.mlist.SetString(i,item)
        self.stack.append(list)   #push last into stack
        self.btnUndo.Enable()

#----------------------------------清空-----------------------------------------
    def OnClear(self,event):
        if self.mlist.GetCount()==0:return
        self.stack.append(self.mlist.GetStrings())
        self.mlist.Clear()
        self.btnUndo.Enable()

#----------------------------------撤销-----------------------------------------
    def OnUndo(self,event):
        try:
            list = self.stack.pop()   #pop from stack
            self.mlist.Clear()
            self.mlist.InsertItems(list,0)
            if len(self.stack)==0:
                self.btnUndo.Disable()
        except IndexError:return True
        
#----------------------------------CRC------------------------------------------
    def OnCRC(self,event):
        p = ur'([\(|\[])([\da-fA-F]{8})([\]|\)])'
        regex = re.compile(p)
        count = self.mlist.GetCount()
        if count==0:return
        list = []
        for i in range(0,count):
            txtA = self.edtText1.GetLineText(0)
            item = self.mlist.GetString(i)
            list.append(item)
            item = regex.sub(u'',item)
            self.mlist.SetString(i,item)
        self.stack.append(list)   #push into stack
        self.btnUndo.Enable()

#--------------------------------正则替换---------------------------------------
    def OnRegex(self,event):
        try:
            p = self.edtRegex.GetLineText(0)
            text = self.edtText3.GetLineText(0)
            regex = re.compile(p)
            count = self.mlist.GetCount()
            if count==0:return
            list = []
            for i in range(0,count):
                txtA = self.edtText1.GetLineText(0)
                item = self.mlist.GetString(i)
                list.append(item)
                item = regex.sub(text,item)
                self.mlist.SetString(i,item)
            self.stack.append(list)   #push into stack
            self.btnUndo.Enable()
        except re.error as err:
            if err[0]=='unbalanced parenthesis': wx.MessageBox(u'正则表达式中的括号不匹配！ ',u'正则表达式错误',wx.OK|wx.ICON_ERROR)
            else: wx.MessageBox(u'正则表达式不正确!\n 错误信息: '+err[0],u'正则表达式错误',wx.OK|wx.ICON_ERROR)

#--------------------------------退出程序---------------------------------------
    def OnExit(self,event):
        self.Close()
#--------------------------------开始操作---------------------------------------
    def OnStart(self,event):
        count = len(self.original)
        for i in range(0,count):
            nameA = self.original[i]
            nameB = self.mlist.GetString(i)
            if nameA != nameB:
                os.rename(self.path+'\\'+nameA, self.path+'\\'+nameB)
    
#--------------------------------程序启动---------------------------------------        
class Query_Gui(wx.App):
    def OnInit(self):
        frame = Query_Frame(None, -1, u"Renaming Tool Python Version")
        self.SetTopWindow(frame)
        frame.Show(True)
        return True


#-------------------------------BASE64文件代码----------------------------------
icoDelete = u'''eJx1TiEOAkEMnEswdavQyPsFT2MtipVU8RTWIe8JCASSEASQkOxNt0Veu9NJZyabAgM7pcS5wjgA
awAjkYgNYbpVxlJlN3N2sjaJo9ZKpfWH1pysTbLxrxKswfviohjC6J4U8axGVH2V2NV9Ofa8qH8u
C5fbCVdiIi5v4P4AXhPwPQG/LbEDPuQn9xv1AzPnhrgfmAEpFT40'''
icoExit = u'''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
MHjewQ=='''
icoPrefix = '''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'''
icoRefresh = '''eJztVk1rE2EQfnbfzSabjZuIzWpEaEz9iB+EIm2ViFQEIaD4A0QkFUqLN8GCSsBcxR+hIJhCzip4
MYh4UvwFQqWHHG0PhQqadebdvOtu3ERbPHjIs5mdzLz7zPsxy8wCGgRyuRxpA2UNmAPIBtkpLCeA
m5qyi1g2gPcmUOZnSIqA5DGaGIamP9hs+oovdtGt0+mQx5M/eJ6v+GIX3wLoRV9PPfXN1VKJdbm9
+ppH2q1nrTOkzfN1POeB9DRtS+JYn36ySlo8KJ1qcYjWq1a7zs/dPvfSfy5d97UIzcpL+EaySbI2
D3QmSbLAl0/k/0rj5OuSvZYENki26b/3hOSNz42eU8oPqoUm0EL2PVrDowkcbZ9G5cV1FD5ew6H1
G5h9t4Dj60sodxdR2VrBhe8PUfvcwKXN+5jzmrj64/HQkx9jjDH+b0TrXAhCj5oJPWpamq4HLmER
bNtSDuE4ZkoIkQwcwjGiQYWsdOFyB/2XJUPrCaE8FEnXNTORCBx7bCedsqyAQrOJbDYSD5moiQFT
4d/W2aKMedGInysGFkm+r3eKPNVrj+o2J7G0Gy7VecWf6a9jyCnFc6kveNQ7ZAwl9om9qVFk5jIv
LNRXpPB/jiFswx3Fp94jhXqUR/3JY58S6llqT7Ew9puH1bMcg/pdz3DTt5JHnOrBxmxDnWmmsu/u
qH3Y8+6UimPY5sLgGs28dSeOZ05YNVKXgzhVt5CdPrDIczJP+fW0iH2LnBl3SZ01b4d96VLuCtuc
E7UmNRaH8DkFsSiPfJ4cQ8UZxuf88Dh9B8i8yXPcWpG5UDkdxZf7pvcknDcW+p6Q8ifub7Bg5CqF
Gn2b9HbM7SPlZjK75f4NtinyxkCNkcJ1pQt8OAu8Tfp1RtYaGutN+vWH68xPUBEwNA=='''
icoReplace = '''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'''
icoStart = '''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'''
icoUndo = '''eJxjYGAEQgEBBiCpwJDBwsAgxsDAoAHEQCGgCEQcBBxYGEYBhSAmLkEtNCyyISo6ziw6NoETJu7q
7s3m7Rsg5+HpaxgWEa2KS79fQHCmk4vHdy9v//uh4VGTrGwcqk0tbA6aW9l9t3N0+efjF/gbaG41
Nr1RMfFqRiYWLy2t7f8FBocejY1LtDOzsNmuo2f8z9zS9p+9o+s/b9/AXyGhkavDI2PcIqPjZDOy
cjkys3O54hOSbbx8AnZGRsX+KSkt356alqkWn5jM6ODk5qdvZPbO1Nz6n62D8z8PL79/gUFh/4Bu
+JeYnPYvPSP7b15+4d/6+sbfXV0911tb22OBfA6Ym5xdPUWA7tlibGr5z9rW8R8wHP75+Qf/i4iK
/ZeQlPIvMyv3X2lZ5YfWto72yqpaQ2z+AurRALr/mZeP/zpf/6CpwHBZDNQ/PyEptSMvv8gnJS2T
n1C8BIVEBAUGh2uB2MGhEUxBIeGMhPSMAgaG///R8AcGhsNAzPwAqoAZiIGh32DPwHASXS0QAwCH
D5Sl'''
icoMain = '''eJztmwlYjt/W8FeDJEnJPKQkFTJGFKGIRhkqc2WsUDKWDMmQKFKEMpQGadA8iQY0PBr8UYa/pDLz
lIdoUuv/rn2nOO8r55z3/a7zXd/3nn1du30Pa+/7t9Zee9977fsJQAhEYcwYoFIcwqUA9ABAWrr1
3KYTQA1da70vD+FKAOY92+7Lg40oAE4GUKE6JAJW0FqPS13gRxL6nilJSEhAt17doLuUNMjKyoJ0
Pxno26cf9BncFwYMGABSI7pCv1HdoMdIGRg0ZBD0Hd4X+k0YCEqTB4KioiKoKCmDsooyqKgqwzAl
FRiurApqI9RAQUMBlLTo/uThMGbsaBgzaiyoq6vDeE110NTShMHGCqAxSwHUjCeApp4mqC6n0lQT
hLYOBfFNyiC0fTh03aIGQk4jQMppNIjuVgfxXeNBaO8kGOA4Bfrs1gYFK3WQX68OGqsngqb9ZFDc
PgaU9k6FSVs1YZr2dJgxTRe01uvCqM0zQcVJF8Y4zwb1Pcago6sDcwxmw2w9fTA0NAQTc2MwMTaF
BQsWgJmlGZibLYLF5kth6dKlsHitIVisswCjbWZgZW0JlpZWYGVpDatWrYJ1NqvBxnYtrF+/Hmy3
24GD/SbYunUrODnvAOcdO2Gniwt0OqANEvu0YNSJCSB6RA9kj80FIW8TED5lDj1PLgHFQ8R2QAeG
uRmBmpsJjHedC6pHLEDD1Qy0jpnBlHNLoHOANfQ6bwNKZ21B/YItaPhvg66BNtAzeAMMCHUE+UAH
GBa+AyZedgJLt7lgvs8SzCLmg9GhNWDmtQEMT64ES3dHMPHdASs9bGGrpwOsPugILgdcQCtvMYy7
ZQ1j8zbDrMK5YJ+1DZZWrQK9l86wz20vuO7dBxoxrqAdfxBcjrmB9bkDsP2EG+w4cwhmRO8DvUR3
WJDoBRbpPuAYsh82Bx2HHbH+sOtaIEx5eACmvfaFZdl+sC73HMx+cRo21pyFjXmB4MQLhTnVEWAs
CIXl9Vdg/pcUWNqYCWu/PYCN3+6BfctzOHDgALgfdofDR9zB/eBhOHzoMHh6esIxb084cdwHjgb4
gK+vL/gGnIIz/n5wxs8fAgIC4NAlL3C97gGul06BW4wveEZdgNNBfuATdhYuBJ4D18QACLx0Afyi
guHotTDwSwyGs2mRcDEjFkJCgiEkMhTCI8IgLDQcIqMiITD2CkTFRkNs7FWIjYmDy8mxEJMYC2GZ
iXD1WiIkJCZAcmoSpKYlQ+KNNEhPT4f9BdFw4F4MeOWmwOn8RDjyIAF8S1MhND8NbmRnwLGqZMjK
ygBf3k24cSsbEnlZEP2cB6n3ciG05D74vnoE3l8egV/ta4h7+wpCmr5Cbl4uFNwvhj8oF5X8AY+f
PIJifjk8q3wGFRXl8LzmDZR9egNv3r6GakE1CD59BH6tAGq/1EJdw1doaKyDlpYWbtz/9ddf8P95
irAw1pbrLS4q2tvk70hazNPTM15ooT1QV3eQuKiQiLhuR5JmJiRpfjWHx5KxnJ6unKSQkJD4gF9K
6pqYRSTl8XhFRUXf5XV0NCRFhETE/kZ+obGunolFTFImtVrEhIuKHrAKhSZyujpykp2ERUV/yJsY
W8Ql5LBGeTz2t5AJlxQV3S0sLDIdNP74teN7d2/T/yFvzFDz8goKiwp5eYVMurSohBJ7yMK+mmGX
Q0MunT84+0f7Obyi5AmqNvdunty50rrowYMHJQ9KSsrZUx4slJtsa6s1Vn3pjh/w83i868OVlJRG
qKmqKA2/94A1Xl5SQQ948MBMd6HpdBkRsk/ED2V5Rc4krrrOxTN+yvB71HhV+UNy3gclRSUW0xaa
6Mh0EhIR7fWzvJOqkupoHhGvWcJQKkoqqioe0mMqPLRn6Qzt07WLRPcf+poVFcWPUtGKL60qKVqn
xqRa08OS8nKPQRMr37+ufJK2R/cn+ZKSvHgeYVQUrV5MjfMrKvh8fkX5w5KKqEFjgoIDz7q7H7L4
4SpF5SUPikpLqvglRasWl1aVM2l+NWnwkB+tu2C7oYKU1OBxP7lWSUkVM0kFv6J09fKqqgqSrebX
0FMq+DGzwvcY9xcVEhKV+0m+qooTr64oWbuctV3Df1b5is+wEvUsPDh5kd7t8uHlVQy2gl9T8XCt
FSfu7eCw5RlVqE7SNdA3GNq3Tx/5/oXt8hVMORKv4ZevXU9Fta/D+vWOPkyJHLmJbz58ePf2eYpR
e/uRVdX8DPutt2sE/Kq165+d9vHe4uDouMXnIz0pX1vxzLkz+932HfihbwS/JsNy8YrNlY98jtjZ
2Tk4rN+yacuWI0+Iq6bION11wZDOnbpJ/ZCP4fPXW66wtNu0xcFqhYNXalZJ6uYjR/w+1tTUCIpM
MuMXDiF9haVj2uVrHm6xtLRbfyqLx9uwpUZQU1tbnPWHQCAg+YfzkjLNtcWFQKhXu8MlVfPtieOm
oFZQteEI/a2lVFdXSxWYfI4FyQsJ9Qpvk8+pEdzbtSuLxATVmzn5OhJn8oLaioX5eYensfZ7erTL
0/Xq6homxrc/SrXqWKqvY/L8hfm88Gms/Z7tDsRjLdO9uvra6i0nWOP1JF5fx7CqF/LuRrS23y5f
RA0y+XqSt/clkLrGusb6Jjqorash543TYe1LL2yTL+GUo1ab6qq9Sb6usam+qamJPaBOYPGgPE6H
m7Da5atquWeTWF31UX8CaWxqaGpubmBK1FqU8BNmkjyIzWuXr2uoZ9DNzfUfT1yob6QDEqczTr6C
nzmHtS/WPuPW1DfUPb5Q2UhNCnweNTU3NrcmaqW+zoNfk2ksKQJCYsbt8g2NZb6+/i+/fnpZ6f/0
e+MtLc1N9fUN9R58Ac9ImuRF9NrkBU3Vj/39Ax6XVT6+4P+suYVkuUQPaGqIrKktNJIhfpH2AV/b
/PpxQMCFstu3X7zgN/4k39TU3BQpqH1g2oPsLzS9Xd2W0rKLFx9/YiKN7dLsjNhiBI0l82VZ+9rf
5SvqW+pvXXz0qlWkpeVv5JsTBU18M1niF5r0Q76lqba++b/Ks3N+bU1JhLa0TO/ebfJVTT/f/142
1Qn4JbykaIvpA6QH9JaR6S83M+q7PJ/J1NcKaqpKCpMS4sIjohMTk3g/hh/cSLwBPydedERMIq8I
/jekv7j02xJhGle6wmBWVgBXNgBXIrSWgl+V0zq4/s/Kd+9Abtp/uv8vKCv+frn3E9lNMPjv2pUr
WZxKoStFrj/FqUI/ddBPcWrnzp2hi3gXkJGhOLWfNPQe1APk5QaDopIiqI5RhUnTJ4HwdhXQ05sF
+vr6YDLXGMwXmcHiRYth0bJFoLvDHIxdLMFqpSVYW1vD2vVrwNbWFtZvtAN7ittcdu6GXS67QX3/
XOh1bjXIhW8F7UvbQTvEBTQi98Ki/bagf9YKjHztYN6FVbDU1xFWUJ4XsA3MQqzB5fxBML5yABbF
esDyeG+wjvaAtcl+YJ8aANszA2FvUQTs27cPDh44BEc9PcDzqBfFMl5w4sQJ8Dt9Evz9/cEt6Cgc
CfKBC0EX4eLFQLgYGQKuqZfANSMMgoODITg0CMLCwriYJIpydPRVCKXYJCgjDuLi4iCeYpKkZIpD
UlO4GCT9Rjpcv54ON27cgAO8SDhWHA+BeakQkZMGWdmZkJabBfEF2ZCUnwURT25D+tNCyM7Ohuyc
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
N57QwW8/O8psnvkP8ZyUDg=='''

app=Query_Gui(0)#redirect=True，重定向输出
app.MainLoop()


