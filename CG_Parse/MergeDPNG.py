# encoding:utf-8
# merge DPNG
import os,re
import Image

filelist = os.listdir(u'./image')
regex = re.compile(r'(?P<prefix>.*)\+DPNG(?P<num>\d{3})\+x(?P<x>\d+)y(?P<y>\d+)')
filedict = {}
f = open('1.txt','w')

for fname in filelist:
	match = regex.search(fname)
	try:
		if not match.group('prefix') in filedict.keys():
			filedict[match.group('prefix')] = [[match.group('num'),match.group('x'),match.group('y')],]
		else:
			filedict[match.group('prefix')].append([match.group('num'),match.group('x'),match.group('y')])
	except:
		pass

for key in filedict.keys():
	flist = filedict[key]
	imgs = []
	for part in flist:
		imgs.append(Image.open('./image/%s+DPNG%s+x%sy%s.png'%(key,part[0],part[1],part[2])))
	width = imgs[0].size[0]
	height = sum([img.size[1] for img in imgs])
	newimg = Image.new('RGBA',(width,height))
	for x in range(0,len(flist)):
		newimg.paste(imgs[x],(int(flist[x][1]),int(flist[x][2])))
	newimg.save('./merged/'+key+'.png')
f.close()

