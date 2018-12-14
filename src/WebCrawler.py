# Created by Yumeng Yang on 12/8/2018
# -*- coding: utf-8 -*-
# https://www.facebook.com/uic.edu
# https://admissions.uic.edu/explore-uic
# https://ampersand.honors.uic.edu
# http://coemakerspace.uic.edu

import urllib.request
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import ssl
import queue
import random
import os

def scraping():
	
	ssl._create_default_https_context = ssl._create_unverified_context
	init_link = "https://www.cs.uic.edu"

	ua = UserAgent(verify_ssl=False)
	print(ua.safari)
	headers = {'User-Agent':ua.random, "Accept-Language": "en-US,en;q=0.5"}
	print(headers)
	q = queue.Queue()
	q.put(init_link)
	visited = set()
	loop = 1
	size = 0
	docNum = 0
	match_index_num = {}
	maxth_index_href = {}
	while docNum < 3000:
		loop+=1
		currLink = q.get().strip('\n')
		if currLink in visited:
			continue
		try:
			print(currLink)
			print(docNum)
			print("processing....")
			# req = Request(currLink)
			# page = urlopen(req, timeout=10).read()
			
			page = urllib.request.urlopen(currLink, timeout = 10).read()
			soup = BeautifulSoup(page,'html.parser')
			fout = open("../output/pages/" + str(docNum), 'w')
			visited.add(currLink)
			for content in soup.find_all(['p','a','title','h1','h2','h3']):
				content = content.get_text()
				content = content.encode('utf-8','ignore')
				fout.writelines(str(content))
				fout.writelines('\n')

			docNum += 1
			match_index_num[docNum] = currLink
			maxth_index_href[currLink] = docNum
			linklist = set()
			for link in soup.find_all('a'):
				href = str(link.get('href')).rstrip("/")
				if 'uic.edu' not in href:
					continue
				if href in visited:
					continue
				if href.startswith('http'):
					size += 1
					q.put(href)
					linklist.add(href)
				if href.startswith('/'):
					root = []
					root += currLink.split("://")
					href = root[0] + "://" + root[1].split("/")[0] + href
					if href not in visited:
						size += 1				
						linklist.add(href)
						q.put(href)
			# print(linklist)
			fout = open("../output/graph", 'a')
			fout.writelines(currLink)
			fout.writelines('\n')
			fout.writelines(str(linklist))
			fout.writelines('\n')
		except:
			pass
	fout = open("../output/match_index_num", 'w')
	fout.writelines(str(match_index_num))
	fout = open("../output/maxth_index_href", 'w')
	fout.writelines(str(maxth_index_href))
	# print(match_index_num)
	# print(maxth_index_href)

if __name__ == '__main__':
	scraping()
