import os,sys
def GetHead(f,count):
    f.seek(0)
    return f.read(count)
if len(sys.argv)==1:
    print 'Drop files on me to rename...'
else:
    try:
        lst = sys.argv[1:]
        #print lst
        for item in lst:
            full = open(item,'rb')
            part = open(item+'.txt','wb')
            part.write(GetHead(full,1000))
            part.close()
            full.close()
            print('Succeeded: '+item+'.txt')
    except Exception as e:
        print e

    finally:
        raw_input('\nPress any key to exit...')
