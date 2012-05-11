import Image

im = Image.open('cave.jpg')
odd = Image.new('RGB',(320,240))
data = im.load()
for j in range(0,240):
    for i in range(0,320):
        odd.putpixel((i,j),data[2*i,2*j])
odd.save('b.jpg')
 