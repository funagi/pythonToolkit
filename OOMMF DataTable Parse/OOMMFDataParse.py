import os,sys,Image
if len(sys.argv)==1:
    print 'Drop files on me to rename...'
else:
    try:
        lst = sys.argv[1:]
        #print lst
        for item in lst:
            intext = open(item).read()
            outtext = open(item+'.csv','w')
            inarray = intext.split('\n\n')
            for indata in inarray:
                inlist = indata.split('\n')
                for inline in inlist:
                    outtext.write(inline+',')
                outtext.write('\n')
            outtext.close()
    except Exception as e:
        print e

    finally:
        raw_input('\nPress any key to exit...')
