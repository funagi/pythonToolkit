import Image,wx,math
import ImageDraw
from vector import *

i = Image.new('RGB',(6000,6000))
d = ImageDraw.Draw(i)
p = vector(1,3,0)
ma = 1
mi = 0
#phi = [[0 for b in range(-300,300)] for b in range(-300,300)]
for x in range(-300,300):
    for y in range(-300,300):
        if x==0 and y==0:continue
        r = vector(x,y,0)
        r2 = (r * (p * r)) * 3
        l = r.length()
        phi = (p - r2*(1/l)).normalize()
        
        x0 = (x+300)*10+5
        y0 = (y+300)*10+5
        d.line((x0,y0,x0+(phi*10)[0],y0+(phi*10)[1]))

i.save('1.jpg',quality=80)
