import re,os
xmax=100
ymax=100
zmax=6
def GetLength(x):
    return (x-49.5)*5
for fname in os.listdir('.'):
    if not '.omf' in fname:
        continue
    f=open(fname)
    output=open('result.csv','a')
    string=''
    #find time
    retime=re.compile(r'\d+(.\d+(e(-|)\d+|)|)')
    while not 'Total simulation time' in string:
            string = f.readline()
    time=retime.search(string).group(0)
    #find core
    while not 'Begin: Data Text' in string:
            string = f.readline()
    maxvalues=[[0,0,0,0]]*zmax
    for z in range(0,zmax):
        for y in range(0,ymax):
            for x in range(0,xmax):
                data=f.readline().split()
                if abs(float(data[2]))>=abs(maxvalues[z][3]):
                    maxvalues[z]=[x,y,z,float(data[2])]
    res='%d,%d,%d,%d,%s,%.1f,%.1f,%.1f,%.1f,%e\n' %(maxvalues[0][0],
     maxvalues[0][1],maxvalues[zmax-1][0],maxvalues[zmax-1][1],
     time,GetLength(maxvalues[0][0]),GetLength(maxvalues[0][1]),
     GetLength(maxvalues[zmax-1][0]),GetLength(maxvalues[zmax-1][1]),
     float(time)/1e-9)
    output.write(res)
output.close()
raw_input('Press Enter to exit...')
