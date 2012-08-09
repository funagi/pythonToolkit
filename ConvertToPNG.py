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
            img.save(name+'png')
            printc(('[%' + str(length) +'d/%' + str(length) + 'd] ') % (lst.index(item)+1,count), 'green', end='')
            print sname+'png'
    except Exception as e:
        printc(e.message,'red')

    finally:
        raw_input('\nPress any key to exit...')

