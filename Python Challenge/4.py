import urllib

s=str(92118/2)
pf = file('out.txt','w')
for i in range(1,400):
    url = 'http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing='+s;
    sock = urllib.urlopen(url);
    sout = sock.read();
    n = sout.find('and the next nothing is ');
    print s,sout;
    print >>pf, s, sout;
    s = sout[n+24:n+29];
    if(n==-1):break
pf.close()
