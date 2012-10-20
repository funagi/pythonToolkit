#coding=utf-8
import Image,re,os

pattern = re.compile(r'(?P<name>\w+)#(?P=name)1@(?P<left>\d+)_(?P<top>\d+)_(?P<width>\d+)x(?P<height>\d+).PNG')
original = os.listdir('.')
index = []
index2 = {}
for pic in original:
    sch = pattern.search(pic)
    print sch
    if not(sch):continue
    if not(sch.group(1) in index):
        index.append(sch.group(1))
        index2[sch.group(1)]=[]
    index2[sch.group(1)].append(sch.groups())
print index2

for img in index2:
    lst = index2[img]
    width=0;height=0
    for subimg in lst:
        if subimg[1]=='0':height+=int(subimg[4])
        if subimg[2]=='0':width+=int(subimg[3])
    image = Image.new('RGBA',(width,height),(255,255,255,255))
    for subimg in lst:
        simg = Image.open('%s#%s1@%s_%s_%sx%s.PNG'%(subimg[0],subimg[0],subimg[1],subimg[2],subimg[3],subimg[4]))
        for x in range(0,int(subimg[3])):
            for y in range(0,int(subimg[4])):
                try:
                    color = simg.getpixel((x,y))
                    if color[3]==0:
                        color=(255,255,255,255)
                    else:
                        color = (color[2],color[1],color[0],255)
                    if subimg[1]=='0' and subimg[2]=='0':
                        image.putpixel((int(subimg[1])-simg.size[0]+(int(subimg[3]))+x,int(subimg[2])-simg.size[1]+(int(subimg[4]))+y),color)
                    if subimg[1]=='0' and subimg[2]=='256':
                        image.putpixel((int(subimg[1])-simg.size[0]+(int(subimg[3]))+x,int(subimg[2])+y),color)
                    if subimg[1]=='256' and subimg[2]=='0':
                        image.putpixel((int(subimg[1])+x,int(subimg[2])-simg.size[1]+(int(subimg[4]))+y),color)
                    if subimg[1]=='256' and subimg[2]=='256':
                        image.putpixel((int(subimg[1])+x,int(subimg[2])+y),color)
                    #print (int(subimg[1]),int(subimg[2]),int(subimg[1])+int(subimg[3]),int(subimg[2])+int(subimg[4]))
                except:
                    continue
    image.save(".\out\%s.png"%img)
    #image.save("%s.png"%img)
    print '%d\t%d\t%s.png saved!' % (width,height,img)
raw_input('over')
