#encoding:utf-8
import re

name = u'倒错的轮舞'
htmlcount = 20
mode = 'multi' # multi
title_regex = re.compile(r'(?:<strong>(<spanclass=".*?">|))(?P<title>.*?)(?:(</span>|)</strong>)',re.IGNORECASE)
content_regex = re.compile(r'(?:<td><divalign="left">)(?P<content>.*?)(?:</div></td>)')
html_regex_close = re.compile(r'</.*?>')
html_regex = re.compile(r'<.*?>')

if mode=='one':
	output = open('./%s.txt'%name,'w')

for i in range(0,htmlcount+1):
	f = open('./%s/zw/mydoc%03d.htm' % (name, i), 'r')
	text = f.read()
	# parse original text
	text = text.replace(' ','').replace('\n','')
	# find content
	try:
		ifmatch = content_regex.search(text)
		if ifmatch:
			text1 = html_regex_close.sub('\n',ifmatch.group('content'))
			text2 = html_regex.sub('',text1)
		iftitle = title_regex.search(text)
		# find title
		if iftitle:
			title = iftitle.group('title')
			title = html_regex.sub('',title)

		if mode=='multi':
			output = open('./%s/%03d.txt'%(name, i),'w')
		output.write(title.decode('gbk').encode('utf-8'))
		output.write('\n')
		output.write(text2.decode('gbk').encode('utf-8'))
		output.write('\n\n')
		if mode=='multi':
			output.close()
	except Exception,e:
		print e,dir(e)
if mode=='one':
	output.close()