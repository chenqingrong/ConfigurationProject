import os
import re
import urllib2
from bs4 import BeautifulSoup

def main():
	link = "https://spark.apache.org/docs/latest/configuration.html"
	req =  urllib2.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
	page = urllib2.urlopen(req)
	content= page.read()
	tables= BeautifulSoup(content,'html.parser').find_all("table")

	names=[]
	description=[]
	values=[]

	for table in tables:
		trs=table.find_all("tr")
		ths=trs[0].find_all("th")
		flag=True
		if len(ths)==2:
			flag=False
		for i in range(1,len(trs)):
			tds=trs[i].find_all("td")
			if flag:
				names.append(tds[0].text)
				values.append(tds[1].text)
				description.append(tds[2].text)
			else:
				names.append(tds[0].text)
				description.append(tds[1].text)
				values.append("N/A")
	f=open("spark-configuration",'w')
	for i in range(len(names)):
			f.write(names[i].replace(u'\u2019','')+'**'+description[i].replace('\n',' ').replace(u'\u2019','')+'**'+values[i].replace('\n',' ').replace(u'\u2019','')+'\n')
	f.close()
main()
