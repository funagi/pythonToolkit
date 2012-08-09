import os,sys,Image
from utils import printc
  
if len(sys.argv)==1:
    printc("Drop files on me to rename...",'red')
    raw_input('\nPress any key to exit...')
else:
    try:
        lst = sys.argv[1:]
        count = len(lst)
        length = len(str(count))
        #print lst
        for item in lst:
            pos = item.rindex('.')+1
            name = item[:pos]
            sname = item[item.rindex('\\')+1:pos]
            img = Image.open(item)
            width,height = img.size
            img = img.crop((6,28,width-6,height-6))
            img.save(name+'jpg',quality=80)
            printc(('[%' + str(length) +'d/%' + str(length) + 'd] ') % (lst.index(item)+1,count), 'green', end='')
            print sname+'jpg'
    except Exception as e:
        printc(e.message,'red')

    finally:
        raw_input('\nPress any key to exit...')
