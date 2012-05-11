#coding=utf-8
import Image,re,os

pattern = re.compile(r'(?P<name>\w+)#(?P=name)@(?P<left>\d+)_(?P<top>\d+)_(?P<width>\d+)x(?P<height>\d+).PNG')
original = os.listdir('.')
index = []
index2 = {}
for pic in original:
    sch = pattern.search(pic)
    if not(sch):continue
    if not(sch.group(1) in index):
        index.append(sch.group(1))
        index2[sch.group(1)]=[]
    index2[sch.group(1)].append(sch.groups())


for img in index2:
    lst = index2[img]
    width=0;height=0
    for subimg in lst:
        if subimg[1]=='0':height+=int(subimg[4])
        if subimg[2]=='0':width+=int(subimg[3])
    image = Image.new('RGBA',(width,height))
    for subimg in lst:
        simg = Image.open('%s#%s@%s_%s_%sx%s.PNG'%(subimg[0],subimg[0],subimg[1],subimg[2],subimg[3],subimg[4]))
        for x in range(0,int(subimg[3])):
            for y in range(0,int(subimg[4])):
                color = simg.getpixel((x,y))
                color = (color[2],color[1],color[0],255)
                image.putpixel((int(subimg[1])+x,int(subimg[2])+y),color)
        #print (int(subimg[1]),int(subimg[2]),int(subimg[1])+int(subimg[3]),int(subimg[2])+int(subimg[4]))
    image.save("E:\Game Files\Remember11 - CG\output_bg\%s.png"%img)
    #image.save("%s.png"%img)
    print '%d\t%d\t%s.png saved!' % (width,height,img)
raw_input()
