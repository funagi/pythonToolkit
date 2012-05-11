import string

sin = '~!@#$%^&*()_+'
#sin = 'map'
#sin='g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr\'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj. '
sout = ''

n=len(sin)
for i in range(0,n-1):
    temp = ord(sin[i]);
    '''if((temp!=32)and(temp!=ord('.'))):
        if((temp==121)or(temp==122)):
            sout += chr(temp-24)
        else:
            sout += chr(temp+2)
    else:
        sout += sin[i]
print sout'''
    print temp
