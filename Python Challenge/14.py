import Image
      
code = Image.open('wire.png')
pw = []
'''
for i in range(0,50):
    n = Image.new('RGB',(4*(99-2*i),1))
    for j in range(0,n.size[0]):
        n.putpixel((j,0), code.getpixel((j,0)))
    n.save('.\\pic\\'+ str(99-2*i) + '.jpg')
print pw
''''''
sum = 0;
out = Image.new('RGB',(100,100))
for i in range(0,49):
    for j in range(i,100-i):
        
        out.putpixel((j,i),code.getpixel((sum+j-i,0)));
        sum+=1;
    for j in range(i+1,100-i):
        out.putpixel((99-i,j),code.getpixel((sum+j-i-1,0)));
        sum+=1;
    for j in range(i,99-i):
        
        out.putpixel((98-j,99-i),code.getpixel((sum+j-i,0)));
        sum+=1;
    for j in range(i+1,99-i):
        out.putpixel((i,99-j),code.getpixel((sum+j-i-1,0)));
        sum+=1;

out.save('1.jpg')
'''
my=Image.new('RGB',(100,100))
f=Image.open('wire.png')
print 'x,y=%d,%d'%(f.size[0],f.size[1])
n=100 
x,y=0,0
i=0
while i<10000:
##		print 'i,n=%d,%d'%(i,n)
		
		for cnt in range(n):
			my.putpixel((x+cnt,y),f.getpixel((i,0)))
			i+=1

		x+=(n-1)
		
		for cnt in range(1,n):
			my.putpixel((x,y+cnt),f.getpixel((i,0)))
			i+=1

		y+=(n-2)
		
		for cnt in range(1,n):
			my.putpixel((x-cnt,y),f.getpixel((i,0)))
			i+=1

		x-=(n-2)
		
		for cnt  in range(1,n-1):
			my.putpixel((x,y-cnt),f.getpixel((i,0)))
			i+=1
		y-=(n-3)

		n-=2 

my.save(ur'14.png','png')