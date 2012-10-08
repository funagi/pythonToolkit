import os,sys,Image
from utils import printc
  
if len(sys.argv)==1:
    printc("Drop files on me to rename...",'red')
    raw_input('\nPress any key to exit...')
else:
    try:
        dirmode = False
        lst = sys.argv[1:]
        count = len(lst)
        length = len(str(count))
        if count==1 and os.path.isdir(lst[0])==True:
            dirname = lst[0]
            lst = [dirname+'\\'+item for item in os.listdir(lst[0])]
            count = len(lst)
            length = len(str(count))
            dirmode = True
        #print lst
        for item in lst:
            try:
                if os.path.isdir(item):raise Exception('Directories should be parsed one by one.')         
                pos = item.rindex('.')+1
                name = item[:pos]
                sname = item[item.rindex('\\')+1:pos]
                img = Image.open(item)
                img.save(name+'jpg',quality=80)
                printc(('[%' + str(length) +'d/%' + str(length) + 'd] ') % (lst.index(item)+1,count), 'green', end='')
                print sname+'jpg'
            except Exception as e:
                printc(('[%' + str(length) +'d/%' + str(length) + 'd] ') % (lst.index(item)+1,count), 'red', end='')
                printc(str(e),'red')
                print
    except Exception as e:
        printc(str(e),'red')

    finally:
        raw_input('\nPress any key to exit...')
