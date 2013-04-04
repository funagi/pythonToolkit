import re,sys

def Bohr(match):
	coef = 0.529
	value = float(match.group())*coef
	return '%.9f'%value
filename = sys.argv[1]
regex = re.compile(r'(?P<num>((-|)\d+.\d+))')

# filename='2222.txt'
# open input file and read text
f = open(filename,'r')
text = f.read()
f.close()
# do the substitution!
newtext = regex.sub(Bohr, text)
# write new text
newfile = open(filename.replace('.txt','.new.txt'), 'w')
newfile.write(newtext)
newfile.close()