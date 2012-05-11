#coding=utf-8
import base64,zlib

lst = ['iDelete.ico','iUndo.ico','iRefresh.ico','iExit.ico','iPrefix.ico','iReplace.ico',
       'iStart.ico','Main.ico']

out = file('b.txt','w')
for f in lst:
    inf = file(f,'rb')
    txt = base64.encodestring(zlib.compress(inf.read()))
    out.write(f+'\n'+txt+'\n\n')

out.close()
