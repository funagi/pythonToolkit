
pf = file('evil2.gfx','rb')
x = pf.read();
for z in range(0,5):
    f2 = file(str(z) + '.jpg','wb');
    
    for i in range(z,67575,5):
        f2.write(x[i]);
    f2.close()
pf.close()