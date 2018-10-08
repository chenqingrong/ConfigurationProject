import os
import re
import urllib2
from bs4 import BeautifulSoup
def deal_with(tmp):
	return tmp.replace(u'\u2019','').replace(u'\u2018','').replace(u'\u2014','').replace(u'\xa0','').replace("\n",' ').replace(u'\u201c',' ').replace(u'\u201d',' ')
def main():
	link= "https://lucene.apache.org/solr/guide/7_0/format-of-solr-xml.html#the-shardhandlerfactory-element"
	req =  urllib2.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
	page = urllib2.urlopen(req)
	content= page.read()
	content=BeautifulSoup(content,'html.parser')
	properties=content.find_all('div',{"class":"sect2"}) 
	names=[]
	description=[]
	value=[]
	for i in range(0,len(properties)-1):
		prop=properties[i]
		content=prop.find('div',{"class":"dlist"}).find("dl").find_all("dt")
		#.find("dl").find_all("dt")
		for c in content:
			names.append(c.text)
			description.append(c.find_next_sibling("dd").text)
			value.append("N/A")
	f=open('solr-configuration','w')
	for i in range(len(names)):
		f.write(deal_with(names[i])+'**'+deal_with(description[i])+'**'+deal_with(value[i])+'\n')
	f.close()
main()