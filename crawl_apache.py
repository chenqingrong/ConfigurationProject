import os
import re
import urllib2
from bs4 import BeautifulSoup

def main():
	link = "https://httpd.apache.org/docs/2.4/mod/core.html"
	req =  urllib2.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
	page = urllib2.urlopen(req)
	content= page.read()
	content= BeautifulSoup(content,'html.parser')
	properties=content.find_all('div')
	names=[]
	information={"Default":[],"Description":[]}
	flag_names=0
	flag_tables=0
	num=0
	for prop in properties:
		ul=prop.find_all('ul')
		tables=prop.find_all('table')
		if flag_names==0 and len(ul)>0:
			for u in ul:
				for li in u.find_all('li'):
					names.append(li.a.string)
				break
			flag_names=1
		if(len(tables)>0 and flag_tables==0):
			for table in tables:
				tr=table.find_all('tr')
				information["Default"].append('N/A')
				information["Description"].append('N/A')
				flag=0	
				for t in tr:
					try:
						if t.th.a.string=='Description:':
							codes=t.td.find_all('code')
							if len(codes)==0:
								information["Description"][-1]=t.td.string
							else:
								information["Description"][-1]=t.td.text
							flag=1
						if t.th.a.string=='Default:':
							information["Default"][-1]=t.td.string
							flag=1
					except:
						flag=2
						information["Default"].pop()
						information["Description"].pop()
						break
				if flag==0:
					information["Default"].pop()
					information["Description"].pop()					
			flag_tables=1
	del information["Description"][0]
	del information["Default"][0]
	print len(names),len(information["Description"]),len(information["Default"])
	f=open('apache-configuration','w')
	for i in range(len(names)):
		f.write(names[i]+'**'+information["Description"][i].replace('\n',' ')+'**'+str(information["Default"][i]).replace('\n',' ')+'\n')
	f.close()
main()