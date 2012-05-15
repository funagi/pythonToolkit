import json,codecs,bz2

fi = codecs.open('data.txt','r','utf-8')
textin = fi.read()

data = []
for text in textin.split('\r\n'):
    array = text.decode('utf-8').split(',')
    if len(array)==2:
        data.append({'label':array[0],'link':array[1]})
    else:
        print 'parameter number not right!'

f = open('output.txt','wb')
s = json.dumps(data)
f.write(s)
f.close()
