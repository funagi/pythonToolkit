#coding=utf-8
import os,sys,Image
if len(sys.argv)==1:
    print 'Drop files on me to rename...'
elif len(sys.argv)!=3:
    print 'Only two pictures can be merged...'
else:
    try:
        lst = sys.argv[1:]
        #print lst
        img1 = Image.open(lst[0])
        img2 = Image.open(lst[1])

        width = img1.size[0]
        height = img1.size[1] + img2.size[1]

        newimg = Image.new('RGBA', (width, height))
        newimg.paste(img1,(0,0,img1.size[0],img1.size[1]))
        newimg.paste(img2,(0,img1.size[1],newimg.size[0],newimg.size[1]))
        newimg.save('%s.png'%lst[0][:lst[0].rindex('\\')+9])
        print('Succeeded: '+'%s.png'%lst[0][:lst[0].rindex('\\')+9])
    except Exception as e:
        print e

    #finally:
        #raw_input('\nPress any key to exit...')
