#encoding=utf-8
import urllib

s=u'http://www.internationalsaimoe.com/img/banners/banner'
for i in range(2,24):
    print 'beginning No.',i,'.......'
    url = s+str(i)+'.jpg'
    print url
    s2=urllib.urlopen(url).read()
    f=file('s'+str(i)+'.jpg','wb')
    f.write(s2)
    f.close()
    print 'No.',i,' finished'
