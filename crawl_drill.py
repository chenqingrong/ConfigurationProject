import os
import re
import urllib2
from bs4 import BeautifulSoup

def main():
	link = "https://drill.apache.org/docs/configuration-options-introduction/"
	req =  urllib2.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
	page = urllib2.urlopen(req)
	content= page.read()
	content= BeautifulSoup(content,'html.parser')
	properties=content.find('table').find("tbody")
	names=[]
	description=[]
	values=[]
	for tr in properties.find_all('tr'):
		tds=tr.find_all('td')
		names.append(tds[0].text)
		values.append(tds[1].text)
		description.append(tds[2].text)
	f=open("drill-configuration",'w')
	for i in range(len(names)):
			f.write(names[i].replace(u'\u2019','')+'**'+description[i].replace('\n',' ').replace(u'\u2019','')+'**'+values[i].replace('\n',' ').replace(u'\u2019','')+'\n')
	f.close()
main()