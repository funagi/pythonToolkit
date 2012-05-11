import pickle,sys

pf = file('banner.p','r')

s=pickle.load(pf)
for c in s:
    for x in c:
        sys.stdout.write(x[1]*x[0]);
    print

pf.close()
