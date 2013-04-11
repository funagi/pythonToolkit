#encoding: utf-8
# merge tachie from Tenshin Ranman LUCKY or UNLUCKY!?
import os,codecs
open = codecs.open
txtdir = u'G:/ext/fgimage/神様'
outputdir = u'G:/ext/fgimagemerge/神様'
output = open('merge.bat','w','utf-8')
output.write('@echo off\r\nchcp 65001\r\nset PATH=E:\Program Files\ImageMagick-6.8.4-8;%PATH%\r\n')
filelist = os.listdir(txtdir)
txtlist = []
infotxtlist = []
for f in filelist:
	if '_info.txt' in f:
		infotxtlist.append(f)
	elif '.txt' in f:
		txtlist.append(f)

typelist = {'dress':[],'face':[]}
for info in infotxtlist:
	f = open(txtdir+'/'+info, 'r', 'cp932')
	for line in f:
		data = line.replace('\r\n','').split('\t')
		if len(data)==5:
			typelist[data[0]].append(data[4])
		elif len(data)==4:
			typelist[data[0]].append(data[3])
	f.close()

typelist['dress'] = list(set(typelist['dress']))
typelist['face'] = list(set(typelist['face']))

filename = {}
prefixes = []
c=0
for txt in txtlist:
	f = open(txtdir+'/'+txt, 'r', 'cp932')
	prefix = unicode(txt.replace('.txt',''))
	prefixes.append(prefix)
	for line in f:
		data = unicode(line).split('\t')
		filename[prefix+data[1]] = [(data[2]),(data[3]),data[9]]
		# print prefix+'_'+data[1],prefix+'_'+data[9]
	f.close()


for prefix in prefixes:
	for dress in typelist['dress']:
		for face in typelist['face']:
			try:
				output.write('composite -geometry +%s+%s "%s/%s.png" "%s/%s.png" "%s/%s.png"\r\n' % (
					str(-int(filename[prefix+dress][0])+int(filename[prefix+face][0])), str(-int(filename[prefix+dress][1])+int(filename[prefix+face][1])), # geometry x and y
					txtdir, '_'.join([prefix,filename[prefix+face][2]]), # overlay image
					txtdir, '_'.join([prefix,filename[prefix+dress][2]]), # base image
					outputdir, '_'.join([prefix,dress,face.replace('?','？')]), # output image
					))
			except Exception:
				pass# print prefix, dress, face
print len(prefixes)*len(typelist['dress'])*len(typelist['face'])
os.system('pause')
output.close()