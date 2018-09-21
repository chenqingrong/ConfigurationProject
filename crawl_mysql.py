import os
import re
import urllib2
from bs4 import BeautifulSoup

def main():
	link = "https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_activate_all_roles_on_login"
	req =  urllib2.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
	page = urllib2.urlopen(req)
	content= page.read()
	content= BeautifulSoup(content,'html.parser')
	divisions= content.find_all('div',{"class" : "itemizedlist"})
	names=[]
	default=[]
	description=[]
	for div in divisions:
		subdivs=div.find_all('div',{"class":"informaltable"})
		if len(subdivs)>0:
			for subdiv in subdivs:
				table=subdiv.find_all("table")[0]
				tr=table.find_all('tr')
				flag_value=0
				flag_system=0
				for t in tr:
					if 'System Variable' in t.text:
						tmp=t.text
						names.append(tmp.replace('System Variable',''))
						flag_system=1
					if 'Default Value' in t.text and flag_value==0 and flag_system==1:
						tmp=t.text
						default.append(tmp.replace('Default Value',''))
						flag_value=1
				if flag_value==0 and flag_system==1:
					default.append('N/A')
				if flag_system==1:
					p=table.find_next('p')
					description.append(p.text)
	f=open('mysql-configuration','w')
	for i in range(len(names)):
		text=description[i].replace(u'\xa0', u' ')
		text=text.replace(u"\u201c", u' ')
		text=text.replace(u"\u201d", u' ')
		text=text.replace(u"\u2014", u' ')
		text=text.replace(u"\u2212", u' ')
		text=text.replace('\n',' ')
		f.write(names[i].replace('\n',' ')+'**'+text+'**'+default[i].replace('\n',' ')+'\n')
	f.close()
main()

