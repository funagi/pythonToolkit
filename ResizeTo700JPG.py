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
            if img.size[0]>700 and img.size[1]>700:
                img.thumbnail((700,700),Image.ANTIALIAS)
            img.save(name+'thumbnail.jpg',quality=80)
            print('Succeeded: '+name+'thumbnail.jpg')
    except Exception as e:
        print e

    finally:
        raw_input('\nPress any key to exit...')
