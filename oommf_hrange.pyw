from math import *;

for i in range(0,361,5):
    ang1 = i*2*pi/360;
    ang2 = i*2*pi/360;
    print '      { %f %f 0 %f %f 0 1 }' % (cos(ang1),sin(ang1),cos(ang2),sin(ang2));
