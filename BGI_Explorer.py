from struct import unpack
import sys

def GetType(string):
    if '@\x00\x00\x00bw' in string:
        return 'Ogg Sound'
    if 'CompressedBG' in string:
        return'Bitmap'
    if 'DSC\x00FORMAT\x001.00' in string:
        return 'DSC FORMAT 1.00'
    return 'Unknown'
    
if len(sys.argv)==1:
    print 'Drop BGI arc packages on me to view...'
else:
    fp = open(sys.argv[1],'rb')
    fp.seek(0)
    head = fp.read(8)
    if head != 'PackFile':
        print 'Not a BGI package!'
        raw_input()
    else:
        try:
            fp.seek(12)
            count = fp.read(4)
            count = unpack('I',count)
            flist = []
            flist2 = []
            for i in range(count[0]):
                list = fp.read(32)
                list = unpack('16sIIII',list)
                flist.append(list)
            for f in flist:
                fp.seek(f[1]+16+32*count[0])
                ftype = fp.read(16)
                flist2.append(f[0].replace('\x00',' ')+'\t'+GetType(ftype))
            log = open(sys.argv[1]+'.log','w')
            log.write('\n'.join(flist2))
            log.close()
        except:
            raw_input()
