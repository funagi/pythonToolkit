
csvdir = 'D:/Animes/evimage/diff'
diffdir = 'D:/Animes/evimage/diff'
basedir = 'D:/Animes/evimage'
outputdir = 'D:/Animes/evimage/results'
f = open(csvdir+'/evdiff.csv','r')
output = open('merge.bat','w')
output.write('@echo off\nset PATH=E:\Program Files\ImageMagick-6.8.4-8;%PATH%\n')
for line in f:
	data = line.split(',')
	output.write('composite -geometry +%s+%s "%s/%s.png" "%s/%s.png" "%s/%s.png"\n'%(data[3],data[4],diffdir,data[2],basedir,data[1],outputdir,data[0]))
	output.write('echo %s.png\n'%data[0])
f.close()
output.write('pause > nul')
output.close()