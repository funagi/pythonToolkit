#encoding:utf-8#
import vector,colorsys,sys
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FixedLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np

def ParseData(data,x,y):
    try:
        num = d.readline().replace('  ',' ')
        if num[0] == ' ':num = num[1:]
        num = [float(value) for value in num.split(' ')]
        vec = vector.vector(num[0],num[1],num[2])
        '''x0 = cell*x; y0 = cell*y
        x1 = x0+hcell; y1 = y0+hcell
        rgb_color0 = colorsys.hsv_to_rgb((vec[0]+1)/2,1,1)
        rgb_color = (int(rgb_color0[0]*255),int(rgb_color0[1]*255),int(rgb_color0[2]*255))'''
        CC[x][y] = vec[2]
    except Exception:
        print x,y,num
        raw_input()

if __name__ == '__main__':
    if len(sys.argv)!=1:
        print 'Drop files on me to rename...'
    else:
        for item in sys.argv:
            item = 'rotating-Oxs_TimeDriver-Magnetization-00-0000220.omf'
            d = open(item,'r')
            cell = 40
            hcell = cell/2-2
            xmax = 100
            ymax = 100
            
            fig = plt.figure(figsize = (20,15),frameon = False)
            ax = fig.gca(projection='3d')
            X = np.arange(0,100,1)
            Y = np.arange(0,100,1)
            X,Y = np.meshgrid(X,Y)
            CC = X * Y
            while(1):
                line = d.readline()
                if 'End: Data Text' in line:break
                if '# Begin: Data Text' in line:
                    for y in range(0,ymax):
                        for x in range(0,xmax):
                            ParseData(d,x,y)
            #设置坐标轴
            ax.w_zaxis.set_visible(False)
            surf = ax.plot_surface(X, Y, CC, rstride=0.5, cstride=0.5, cmap=cm.jet, linewidth=0, antialiased=True)
            plt.savefig('aaa.png',transparent=True)
            d.close()
            print 'Finished : ',item
    
