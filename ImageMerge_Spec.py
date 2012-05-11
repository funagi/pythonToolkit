#coding=utf-8
import Image,ImageDraw,ImageFont
count = 277
left = 'free layer'
right = 'pinned layer'
minvalue = -200
maxvalue = 200

textfont = ImageFont.truetype('cambriai.ttf',30)
for i in range(0,count):
    try:
        img1 = Image.open('up%03d.png'%i)
        img2 = Image.open('down%03d.png'%i)

        width = img1.size[0] + img2.size[0]
        height = img1.size[1] + 100# + img2.size[1]

        newimg = Image.new('RGBA', (width, height),(255,255,255))
        newimg.paste(img1,(0,0,img1.size[0],img1.size[1]))
        newimg.paste(img2,(img1.size[0],0,img1.size[0]+img2.size[0],img2.size[1]))

        draw = ImageDraw.Draw(newimg)
        
        textrect = draw.textsize(left,font = textfont)
        draw.text((250-textrect[0]/2,500), left, fill = (0,0,0), font = textfont)
        textrect = draw.textsize(right,font = textfont)
        draw.text((750-textrect[0]/2,500), right, fill = (0,0,0), font = textfont)
        draw.line((10,570,990,570), fill = (0,0,0))

        rect_center = 15+975*i/count
        draw.rectangle((rect_center-5,565,rect_center+5,575), fill = (0,0,0))
        
        newimg.save('Mov%03d.png'%i)
        print('Succeeded: '+'Mov%03d.png'%i)
    except Exception as e:
        print e

    #finally:
        #raw_input('\nPress any key to exit...')
