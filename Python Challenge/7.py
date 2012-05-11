import Image

arr = []
brr = []
pf = Image.open('oxygen.png')
pix = pf.load()
print pf.size
for i in range(1,629,7):
    arr.append(chr(pix[i,46][0]))
print ''.join([x for x in arr])
print ''.join([chr(x) for x in [105, 110, 116, 101, 103, 114, 105, 116, 121]])