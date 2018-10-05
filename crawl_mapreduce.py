import os
import re
import urllib2
from bs4 import BeautifulSoup

def main():
	link="https://hadoop.apache.org/docs/current/hadoop-mapreduce-client/hadoop-mapreduce-client-core/mapred-default.xml"
	req =  urllib2.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
	page = urllib2.urlopen(req)
	content= page.read()
	content=BeautifulSoup(content,'lxml')
	properties=content.find_all('property')
	result=[[],[],[]]
	for prop in properties:
		names=prop.find_all('name')
		values=prop.find_all('value')
		descriptions=prop.find_all('description')
		if(len(names)>0 and names[0].get_text()!=''):
			result[0].append(names[0].get_text())
		else:
			result[0].append('N/A')
		if(len(values)>0 and values[0].get_text()!=''):
			result[1].append(values[0].get_text())
		else:
			result[1].append('N/A')
		if(len(descriptions)>0 and descriptions[0].get_text()!=''):
			result[2].append(descriptions[0].get_text().replace('\n',' '))
		else:
			result[2].append('N/A')
	f=open('mapreduce-configuration','w')
	for i in range(len(result[0])):
		f.write(result[0][i]+'**'+result[2][i]+'**'+result[1][i].replace('\n',' ')+'\n')
	f.close()
main()