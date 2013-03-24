#encoding:utf-8
import Image,sys,getopt

def usage():
	print 'Usage: CutImage.py <-x 6> <-y 6> [-s] <filename>'

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "x:y:s", ["square",])
	except getopt.GetoptError, err:
		# print help information and exit:
		usage()
		print str(err) # will print something like "option -a not recognized"
		sys.exit(2)

	square = False
	nx = 6
	ny = 6
	for o, a in opts:
		if o in ("-s", "--square"):
			square = True
		elif o == '-x':
			nx = int(a)
		elif o == '-y':
			ny = int(a)
		else:
			assert False, "unhandled option: "+o

	filename = args[0]

	img = Image.open(filename)
	[sx,sy] = img.size

	for x in xrange(0,nx):
		for y in xrange(0,ny):
			newimg = img.crop([sx/nx*x,sy/ny*y,sx/nx*(x+1),sy/ny*(1+y)])
			if square:
				[nsx,nsy] = newimg.size
				center = int(min(newimg.size)/2)
				newimg = newimg.crop([nsx/2-center, nsy/2-center, nsx/2+center, nsy/2+center])
			newimg.save('%s_%d_%d.png'%(filename,y+1,x+1),quality=80)

if __name__=='__main__':
	main()