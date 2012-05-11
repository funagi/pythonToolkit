import Image
n=0
d = [0]*640
im = Image.open('mozart.gif')
ne = Image.new('P',(640,480))
data = im.load()
#print data[86,19],data[87,19],data[88,19],data[89,19],data[90,19],data[91,19],data[92,19],data[93,19]
for y in range(0,480):
    for x in range(0,640):
        if(data[x,y]==195): 
            for q in range(x,640):
                ne.putpixel((q-x,y),data[q,y])
            for w in range(0,x):
                #print w,x,y
                ne.putpixel((640-x+w,y),data[w,y])
                

ne.save('1.png')