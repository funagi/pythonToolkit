#encoding:utf-8#
import Image,vector,ImageDraw,colorsys,sys

def ParseData(data,x,y):
    try:
        num = d.readline().replace('  ',' ')
        if num[0] == ' ':num = num[1:]
        num2 = num
        num = [float(value) for value in num.split(' ')]
        vec = vector.vector(num[0],num[1],num[2])
        vec = vec.normalize()
        x0 = cell*x; y0 = cell*y
        x1 = x0+hcell; y1 = y0+hcell
        rgb_color0 = colorsys.hsv_to_rgb((vec[0]+1)/2,1,1)
        rgb_color = (int(rgb_color0[0]*255),int(rgb_color0[1]*255),int(rgb_color0[2]*255))
        draw.rectangle([(x0,y0),(x0+cell,y0+cell)],fill = rgb_color)
        draw.line((x1-(vec*hcell)[0],y1+(vec*hcell)[1],x1+(vec*hcell)[0],y1-(vec*hcell)[1]))
        
        arrow1 = vec.rotateZ(20)*(-hcell)
        arrow2 = vec.rotateZ(340)*(-hcell)
        
        draw.polygon((x1+(vec*hcell)[0],y1-(vec*hcell)[1],x1+(vec*hcell)[0]+arrow1[0],y1-(vec*hcell)[1]+arrow1[1],
                      x1+(vec*hcell)[0]+arrow2[0],y1-(vec*hcell)[1]+arrow2[1]), fill = (255,255,255))
    except Exception as e:
        print e
        raw_input()

if __name__ == '__main__':
    if len(sys.argv)==1:
        print 'Drop files on me to rename...'
    else:
        for item in sys.argv[1:]:
            d = open(item,'r')
            cell = 40
            hcell = cell/2-2
            xmax = 15
            ymax = 15
            p = Image.new('RGB',(cell*xmax,cell*ymax))
            draw = ImageDraw.Draw(p)
            while(1):
                line = d.readline()
                if 'End: Data Text' in line:break
                if '# Begin: Data Text' in line:
                    for y in range(0,ymax):
                        #print y
                        for x in range(0,xmax):
                            ParseData(d,x,y)
            p.save(item.replace('.omf','.png'))
            d.close()
            print 'Finished : ',item
    raw_input()
