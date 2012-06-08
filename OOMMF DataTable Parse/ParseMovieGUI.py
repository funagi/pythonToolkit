from Tkinter import *
from ttk import *

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
        self.label = Label(self, text = 'Folder:')
        self.label.grid(row=self.i, column=0, sticky=W)
        self.edtFolder = Entry(self)
        self.edtFolder.grid(row=self.i, column=1, sticky=W+E)
        self.i+=1
        
        self.label = Label(self, text = 'Basename:')
        self.label.grid(row=self.i, column=0, sticky=W)
        self.edtBase = Entry(self)
        self.edtBase.grid(row=self.i, column=1, sticky=W+E)
        self.i+=1
        
        self.label = Label(self, text = 'Filename Stepsize:')
        self.label.grid(row=self.i, column=0, sticky=W)
        self.edtStep = Entry(self)
        self.edtStep.grid(row=self.i, column=1, sticky=W+E)
        self.edtStep.insert(0,'50')
        self.i+=1
        
        self.label = Label(self, text = 'File Count:')
        self.label.grid(row=self.i, column=0, sticky=W)
        self.edtCount = Entry(self)
        self.edtCount.grid(row=self.i, column=1, sticky=W+E)
        self.i+=1
        
        self.label = Label(self, text = 'Left Text:')
        self.label.grid(row=self.i, column=0, sticky=W)
        self.edtLeft = Entry(self)
        self.edtLeft.grid(row=self.i, column=1, sticky=W+E)
        self.edtLeft.insert(0,'z=1 layer')
        self.i+=1
        
        self.label = Label(self, text = 'Right Text:')
        self.label.grid(row=self.i, column=0, sticky=W)
        self.edtRight = Entry(self)
        self.edtRight.grid(row=self.i, column=1, sticky=W+E)
        self.edtRight.insert(0,'z=2 layer')
        self.i+=1
        
        self.label = Label(self, text = 'OOMMF Script Path:')
        self.label.grid(row=self.i, column=0, sticky=W)
        self.edtOMF = Entry(self)
        self.edtOMF.grid(row=self.i, column=1, sticky=W+E)
        self.edtOMF.insert(0,'E:\\oommf12a4\\oommf.tcl')
        self.i+=1
        
        self.label = Label(self, text = 'FFMpeg Path:')
        self.label.grid(row=self.i, column=0, sticky=W)
        self.edtFFMpeg = Entry(self)
        self.edtFFMpeg.grid(row=self.i, column=1, sticky=W+E)
        self.edtFFMpeg.insert(0,'E:\\ffmpeg.exe')
        self.i+=1

        
        self.btnStart = Button(self)
        self.btnStart['text'] = u'  Start  '
        #self.btnStart['font'] = u'宋体 8'
        self.btnStart['command'] = self.Start
        self.btnStart.grid(row=self.i, column=0, columnspan=2)
        self.i+=1

        
        
        self.pack()
        
        
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.pack(expand = YES, fill = BOTH)
        self.master.title('Index Local Version')
        self.master.iconbitmap('ParseMovieGUI.ico')
        self.createWidgets()
        
    def ParseFileName(dir,str1,str2,ext):
        flist = os.listdir(dir)
        for f in flist:
            if not ext in f:
                continue
            try:
                os.rename(dir+f,dir+f.replace(str1,str2))
            except Exception as e:
                print e
                
    def PromptError(self, msg):
        print msg
        
    def Start(self):
        #create progress widgets
        self.label = Label(self, text = 'Progress:')
        self.label.grid(row=self.i, column=0, sticky=W)
        self.prog = Progressbar(self)
        self.prog.grid(row=self.i, column=1, sticky=W+E)
        self.pack()
        #Start working!
        
        #get parameters
        folder = self.edtFolder.get()
        oommf = self.edtOMF.get()
        ffmpeg = self.FFMpeg.get()
        basename = self.edtBase.get()
        factor = self.edtStep.get()
        count = self.edtCount.get()
        left = self.edtLeft.get()
        right = self.edtRight.get()
        minvalue = -200
        maxvalue = 200
        #see if parameters are right
        if folder[len(folder)-1]=='\\':
            folder = folder[:len(folder)-1]
        
        #code from ParseMovie.py
        #Parse .omf files with oommf avf2ppm
        os.system('pushd %s' % folder)
        os.mkdir('%s\\Movie' % folder)
        os.system('tclsh84 %s avf2ppm -config 1.config -format B24 -ipat *.omf' % oommf)
        self.ParseFileName('%s\\'%folder,basename,'up','bmp')
        os.system('move *.bmp Movie\\')

        os.system('tclsh84 %s avf2ppm -config 2.config -format B24 -ipat *.omf' % oommf)
        self.ParseFileName('%s\\'%folder,basename,'down','bmp')
        os.system('move *.bmp Movie\\')

        #Code from MergeImage_Spec.py
        errors=[]
        redpoint=[]
        textfont = ImageFont.truetype('cambriai.ttf',30)
        for i in range(0,count):
            try:
                img1 = Image.open('Movie\\up%05d.bmp'%(i*factor))
                img2 = Image.open('Movie\\down%05d.bmp'%(i*factor))

                width = img1.size[0] + img2.size[0]
                height = img1.size[1] + 101# + img2.size[1]

                newimg = Image.new('RGBA', (width, height),(255,255,255))
                newimg.paste(img1,(0,0,img1.size[0],img1.size[1]))
                newimg.paste(img2,(img1.size[0],0,img1.size[0]+img2.size[0],img2.size[1]))

                draw = ImageDraw.Draw(newimg)
                
                textrect = draw.textsize(left,font = textfont)
                draw.text((width/4-textrect[0]/2,height-100), left, fill = (0,0,0), font = textfont)
                textrect = draw.textsize(right,font = textfont)
                draw.text((width*3/4-textrect[0]/2,height-100), right, fill = (0,0,0), font = textfont)
                draw.line((10,height-25,width-10,height-25), fill = (0,0,0))

                rect_center = 15+(width-25)*i/count
                draw.rectangle((rect_center-5,height-30,rect_center+5,height-20), fill = (0,0,0))

                #draw keypoints
                if i in redpoint:
                    draw.rectangle((rect_center-2,568,rect_center+2,572), fill = (255,0,0))
                
                newimg.save('Movie\\Mov%03d.png'%(i))
                print('Succeeded: '+'Mov%03d.png'%(i))
            except Exception as e:
                errors.append(i)
                print e

        if len(errors)!=0:
            print 'Errors:',str(errors)

        #Make mp4 file with ffmpeg
        print '%s -r 15 -i Movie\\Mov%%03d.png out.mp4' % ffmpeg
        os.system('%s -r 15 -i Movie\\Mov%%03d.png out.mp4' % ffmpeg)
        
        
root = Tk()
app = Application(master = root)
app.mainloop()
root.destroy()
