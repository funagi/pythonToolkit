import sys, getopt

def usage():
	print 'Usage: CutOVF.py [-x xrange] [-y yrange] [-z zrange] <OVF filename>'

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "x:y:", [])
	except getopt.GetoptError, err:
		# print help information and exit:
		usage()
		print str(err) # will print something like "option -a not recognized"
		sys.exit(2)

	x1 = 0
	y1 = 0
	x2 = 0
	y2 = 0
	z1 = 0
	z2 = 0
	for o, a in opts:
		if o == '-x':
			data = a.split(':')
			x1 = int(data[0])
			x2 = int(data[1])
		elif o == '-y':
			data = a.split(':')
			y1 = int(data[0])
			y2 = int(data[1])
		elif o == '-z':
			data = a.split(':')
			z1 = int(data[0])
			z2 = int(data[1])
		else:
			assert False, "unhandled option: "+o
	# parameter check
	if x1>x2 or y1>y2 or z1>z2:
		assert False, "illegal xyz range."
	if x1**2 + y1**2 + z1**2 + x2**2 + y2**2 + z2**2 == 0:
		assert False, "There's no need to cut this OVF File."

	filename = args[0]
	newfilename = filename.replace('.omf','[%d~%d,%d~%d].omf'%(x1,x2,y1,y2))
	f = open(filename, 'r')
	nf = open(newfilename, 'w')
	dim = {}
	stepsize = {}
	count = 0
	for line in f:
		if line[0]=='#':
			if 'nodes:' in line:
				data = line.replace('nodes','').replace(' ','').replace('#','').split(':')
				dim[data[0]] = int(data[1])
				nf.write('# %snodes: %d\n'%(data[0],eval('%s2-%s1+1'%(data[0],data[0],))))
			elif 'stepsize:' in line:
				data = line.replace('stepsize','').replace(' ','').replace('#','').split(':')
				stepsize[data[0]] = float(data[1])
				nf.write(line)
			elif 'max:' in line:
				data = line.replace('max','').replace(' ','').replace('#','').split(':')
				nf.write('# %smax: %e\n'%(data[0],eval('(%s2-%s1+1)*stepsize["%s"]'%(data[0],data[0],data[0]))))
			else:
				nf.write(line)
		else:
			count+=1
			z = count/(dim['y']*dim['x'])
			xy = count%(dim['y']*dim['x'])
			x = xy%dim['y']
			y = xy/dim['y']
			if x>=x1 and x<=x2 and y>=y1 and y<=y2 and z>=z1 and z<=z2:
				nf.write(line)
	f.close()
	print dim
	nf.close()

if __name__=='__main__':
	main()