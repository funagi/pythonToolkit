# Convert CPS pictures in 11eyes Cross Over to PNG
from struct import unpack
from os import listdir
import Image

flist = listdir('.')
for f in flist:
	if not '.cps' in f:
		continue
	fp=open(f,'rb')
	print f
	header = fp.read(8)
	[width,height,unknown] = unpack('hhi',header)
	img = Image.new('RGBA',(width,height))
	for y in range(0,height):
		for x in range(0,width):
			p = fp.read(4)
			color = (ord(p[1]),ord(p[2]),ord(p[3]),ord(p[0]))
			img.putpixel((x,y),color)
	img.save(f.replace('.cps','.png'))
	fp.close()