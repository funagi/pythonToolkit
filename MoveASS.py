#coding=utf-8
import os,codecs

original = raw_input('original text:')
changed = raw_input('changed text:')

if original == '':original = u'0000,0000,0000'
if changed == '':changed = u'0000,0000,0050'

print original,changed

filelist = os.listdir('.')
for f in filelist:
    if '.jp.ass' in f:
        fl = codecs.open(f,'r+','utf-16')
        text = fl.read()
        print original in text
        text = text.replace(original,changed)
        fl.seek(0)
        fl.write(text)
        fl.close()
print 'All Done!'
