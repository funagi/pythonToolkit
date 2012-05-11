import os,sys,Image
if len(sys.argv)==1:
    print 'Drop files on me to cut...'
else:
    try:
        lst = sys.argv[1:]
        #print lst
        for item in lst:
            pos = item.rindex('.')+1
            name = item[:pos]
            img = Image.open(item)
            if img.size != (1280,800):continue
            img = img.crop((0,40,1280,760))
            img.save(name+'png')
            print('Succeeded: '+name+'png')
    except Exception as e:
        print e

    finally:
        raw_input('\nPress any key to exit...')
