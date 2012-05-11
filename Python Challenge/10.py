a = ['1','11']#,'21','1211','111221','312211']

temp = ''
cache = ''
count = 1
for i in range(2,31):
    for j in range(0,len(a[i-1])):
        b = a[i-1];
        temp = b[j];
        #print b,temp,b[j],b[j-1]
        #if(j==0):continue;
        if(j==len(a[i-1])-1):
            cache += str(count) + temp;
            continue
        if(b[j] == b[j+1]):
            count+=1
        else:
            cache += str(count) + temp;
            #print cache,count,temp
            count = 1
    a.append(cache);
    cache = '';
    count = 1
for i in range(0,31):
    print 'a[' , i , '] :\t' , len(a[i])
