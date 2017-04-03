#!/usr/bin/python
import json, requests
first=raw_input('First name? ')
last=raw_input('Last name? ')
cell=raw_input('Cell #? ')
zip=raw_input('ZipCode? ')
email=raw_input('eMail? ')

session=requests.session()
url='https://api-proxy.chipotle.com/ri2k17/reg'
headers={
	'Accept':'application/json',
	'Accept-Encoding':'gzip, deflate, br',
	'Accept-Language':'en-US,en;q=0.8',
	'Connection':'keep-alive',
	'Content-Type':'application/json',
	'Host':'api-proxy.chipotle.com',
	'Origin':'https://spottheimposter.chipotle.com',
	'Referer':'https://spottheimposter.chipotle.com/',
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'
}
data={
	'f': first,
	'l': last,
	'm': cell,
	's': "true",
	'z': zip,
	'e': email,
	'es': "true"
}
r=session.post(url,json=data,headers=headers)
print r.json()
