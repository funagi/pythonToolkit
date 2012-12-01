#encoding=utf8
import os
import json
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import datetime

token = '316da1df9dfea24e8285a5574d3d9e64'.replace('3','t')#'125B999464194769AC72CCC42E4DB8FA'

sha256 = SHA256.new()
sha256.update(token)
array = sha256.digest()
#print repr(array), len(array)
key = array
vec = array[16:]

crypt = AES.new(key, AES.MODE_CBC, vec)
data = open('DAYNOW.htm', 'r').read().decode('base64')
datajson = crypt.decrypt(data)#34640
txt = datajson.decode('utf-8')
# f2 = open('out.txt','w')
# f2.write(json.loads(datajson))
# f2.close()
try:
	d = json.loads(txt)
except:
	txt = txt.replace(txt[len(txt)-1],'')
	d = json.loads(txt)
print d.keys(),type(d['day'])
a=datetime.date(2012,11,27)
b=datetime.date(2012,11,27)
print a==b
# for q in d['data']:
# 	print q['xzqmc'],q['xzqdm']

# 纬度			wd 32.057222
# AQI等级		aqidj III
# AQI评定		aqipd 轻度污染
# 站点代码		zddm 20
# 出行建议		cxzs 儿童、老年人及心脏病、呼吸系统疾病患者应减少长时间、高强度的户外锻炼
# 行政区名称	xzqmc 南京
# 健康建议		jkzs 易感人群症状有轻度加剧，健康人群出现刺激症状
# AQI指数		aqiz 115
# 首要污染物	sywrw PM2.5 
# 经度			jd 118.748611
# 行政区代码	xzqdm 320100
# 站点名称		zdmc 草场门