import os
import re
import urllib2
from bs4 import BeautifulSoup

def get_parameters()
def main():
	link_base = "https://serverfault.com/search?q="
	link=link_base
	application=['hdfs-configuration',]
	configurations={}
	for app_one in application:
		for app_two in application:
			if app_two==app_one:
				continue
			else:
				link=link_base
				for parameter_one in configurations[app_one]:
					for parameter_two in configurations[app_two]:
						link+=parameter_one+' '+parameter_two
						req =  urllib2.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
						page = urllib2.urlopen(req)
						content= page.read()
						content= BeautifulSoup(content,'html.parser')

main()