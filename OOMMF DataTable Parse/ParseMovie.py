import os
import Image,ImageDraw,ImageFont
#Basic Parameters
oommf = 'E:\\oommf12a4\\oommf.tcl'
ffmpeg = 'E:\\ffmpeg.exe'
basename = 'space-5e-009-Oxs_TimeDriver-Magnetization-00-00'
factor = 50
count = 901
left = 'z=0 layer'
right = 'z=3 layer'
minvalue = -200
maxvalue = 200
#Batch rename function
def ParseFileName(dir,str1,str2,ext):
    flist = os.listdir(dir)
    for f in flist:
        if not ext in f:
            continue
        try:
            os.rename(dir+f,dir+f.replace(str1,str2))
        except Exception as e:
            print e

#Parse .omf files with oommf avf2ppm
#os.mkdir('Movie')
os.system('tclsh84 %s avf2ppm -config 1.config -format B24 -ipat *.omf' % oommf)
ParseFileName('.\\',basename,'up','bmp')
os.system('move *.bmp Movie\\')

os.system('tclsh84 %s avf2ppm -config 2.config -format B24 -ipat *.omf' % oommf)
ParseFileName('.\\',basename,'down','bmp')
os.system('move *.bmp Movie\\')

raw_input('Process Finished ...')

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
