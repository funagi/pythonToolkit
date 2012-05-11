import os,sys
if len(sys.argv)==1:
    print 'Drop files on me to rename...'
else:
    try:
        lst = sys.argv[1:]
        #print lst
        for item in lst:
            pos = item.rindex('\\')+1
            name = item[pos:]
            namenew = name.decode('shift-JIS')
            print name,'\t--->\t',namenew
            os.rename(item,item[:pos]+namenew)
    except e as Exception:
        print e

    finally:
        raw_input('\nPress any key to exit...')
