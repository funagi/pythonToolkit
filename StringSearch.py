#coding=utf-8
import os,sys

string = '中央人民'.decode().encode('gbk')#'\xbb\xeb\xe3\xe7'#\xb5\xc4\xba\xa3'
not_found = True
flist = os.listdir('.')
for script in flist:
    f = open(script,'rb').read()
    if string in f:
        print script
        not_found = False
if not_found:print 'not found!'

