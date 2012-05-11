import zipfile
s2='90052'
history = []
pf = zipfile.ZipFile('channel.zip','r')
for i in range(0,910):
    history.append(s2);
    s = pf.read(s2+'.txt');
    n = s.find('Next nothing is ');
    print s2,':\t ',s;
    s2 = s[n+16:n+21];
    if(n==-1):break;
print ''.join([pf.getinfo(j+'.txt').comment for j in history])    
pf.close()
