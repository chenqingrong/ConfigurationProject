import os
import re
import urllib2
from bs4 import BeautifulSoup

def deal_with(tmp):
	return tmp.replace(u'\u2019','').replace(u'\u2014','').replace(u'\xa0','').replace("\n",' ')
def main():
	content= open("example_new.html",'r')
	content= BeautifulSoup(content,'html.parser').find("script",{"id":"configuration-template","type":"text/x-handlebars-template"})
	content=content.get_text()
	content= BeautifulSoup(content,"html.parser")
	tables=content.find_all("table")
	names=[]
	description=[]
	values=[]
	for table in tables:
		trs=table.find("tbody").find_all("tr")
		for i in range(1,len(trs)):
			tds=trs[i].find_all("td")
			if tds[0].text not in names:
				if len(tds)>3:
					names.append(tds[0].text)
					description.append(tds[1].text)
					values.append(tds[3].text)
				else:
					names.append(tds[0].text)
					description.append(tds[2].text)
					values.append(tds[1].text)
			else:
				continue
	f=open("kafka-configuration",'w')
	for i in range(len(names)):
			f.write(deal_with(names[i])+'**'+deal_with(description[i])+'**'+deal_with(values[i])+'\n')
	f.close()
main()

#<script id="configuration-template" type="text/x-handlebars-template">