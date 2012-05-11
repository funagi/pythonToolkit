import os,sys,Image
if len(sys.argv)==1:
    print 'Drop files on me to rename...'
else:
    try:
        lst = sys.argv[1:]
        #print lst
        for item in lst:
            pos = item.rindex('.')+1
            name = item[:pos]
            img = Image.open(item)
            img.save(name+'jpg',quality=80)
            print('Succeeded: '+name+'jpg')
    except Exception as e:
        print e

    finally:
        raw_input('\nPress any key to exit...')
