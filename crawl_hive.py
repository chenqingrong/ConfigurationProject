import os
import re
import urllib2
from bs4 import BeautifulSoup

def main():
	link="https://cwiki.apache.org/confluence/display/Hive/Configuration+Properties#ConfigurationProperties-HiveConfigurationProperties"
	req =  urllib2.Request(link, headers={'User-Agent': 'Mozilla/2.0'})
	page = urllib2.urlopen(req)
	content= page.read()
	content=BeautifulSoup(content,'lxml')
	properties=content.find('div',{'class':'wiki-content',"id":"main-content"})
	parameters=properties.find_all('h5')
	result=[[],[],[]]
	for element in parameters:
		name=element.get('id').replace("ConfigurationProperties-",'')
		if(len(name)>0 and name!=''):
			result[0].append(name)
		else:
			result[0].append('N/A')
		value=""
		if(len(value)>0 and value[0]!=''):
			result[1].append(value)
		else:
			result[1].append('N/A')
		descriptions=""
		if(len(descriptions)>0 and descriptions[0].get_text()!=''):
			result[2].append(descriptions[0].get_text().replace('\n',' '))
		else:
			result[2].append('N/A')
	f=open('hive-configuration','w')
	for i in range(len(result[0])):
		f.write(result[0][i]+'**'+result[2][i]+'**'+result[1][i].replace('\n',' ')+'\n')
	f.close()
main()