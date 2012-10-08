# encoding=utf-8

txtfile = open('cernet.txt','r')
action = open('cernet.action','w')

def writerule(prefix='', start=0, length=255, dot=True):
	rule = ''
	for i in range(start,start+length+1):
		if dot:
			action.write('%s.%d.\n' % (prefix, i));
		else:
			action.write('%s.%d\n' % (prefix, i));

# build actionsfile head
action.write('{direct}\n')
sum=0

# read cernet list
for line in txtfile:
	data = line.split()
	data1 = [int(x) for x in data[0].split('.')]
	#print data1
	data2 = [int(x) for x in data[1].split('.')]
	if data2[3]==255:
		if data2[2]==255:
			if data2[1]==255:
				print 'warning!'
			else:
				writerule(data1[0],data1[1],data2[1])
		else:
			writerule('%d.%d'%(data1[0],data1[1]),data1[2],data2[2])
	else:
		writerule('%d.%d.%d'%(data1[0],data1[1],data1[2]),data1[3],data2[3],False)

# close all opened files
txtfile.close()
action.close()