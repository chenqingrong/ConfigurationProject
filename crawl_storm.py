import os
import re
import urllib2
from bs4 import BeautifulSoup
def deal_with(tmp):
	return tmp.replace(u'\u2019','').replace(u'\u2018','').replace(u'\u2014','').replace(u'\xa0','').replace("\n",' ').replace(u'\u201c',' ').replace(u'\u201d',' ')
def main():
	link = "http://storm.apache.org/releases/1.0.6/javadocs/org/apache/storm/Config.html"
	req =  urllib2.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
	page = urllib2.urlopen(req)
	content= page.read()
	content= BeautifulSoup(content,'html.parser')
	table= content.find('table',{"class" : "memberSummary"})
	trs=table.find_all("tr")
	names=[]
	default=[]
	description=[]
	for i in range(1,len(trs)):
		tds=trs[i].find_all('td')
		div=tds[1].find("div")
		names.append(tds[1].find("code").text)
		if div!=None:
			description.append(div.text)
		else:
			description.append('N/A')
		default.append('N/A')
	f=open('storm-configuration','w')
	for i in range(len(names)):
		f.write(deal_with(names[i])+'**'+deal_with(description[i])+'**'+deal_with(default[i])+'\n')
	f.close()
main()

