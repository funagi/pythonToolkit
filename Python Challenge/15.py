import datetime

for i in range(0,100):
    d = datetime.datetime(1006+10*i,1,26)
    if(d.weekday()==0 and ((1006+10*i) % 4 == 0)): print 1006+10*i
