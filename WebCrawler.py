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
	# init_link = "http://www.uicflames"
	# init_link = "http://coemakerspace.uic.edu"

	ua = UserAgent(verify_ssl=False)
	print(ua.safari)
	headers = {'User-Agent':ua.random}
	print(headers)
	q = queue.Queue()
	q.put(init_link)
	visited = set()
	loop = 1
	size = 0
	docNum = 0
	matchtable = {}
	while q.qsize() > 0 or len(visited) > 3000:
		print(loop)
		currLink = q.get().strip('\n')
		try:
			print("no")		
			print(currLink)
			print("yes")
			# req = Request(currLink)
			# page = urlopen(req, timeout=10).read()
			page = urllib.request.urlopen(currLink, timeout = 10).read()
			soup = BeautifulSoup(page,'html.parser')
			fout = open("./output/" + str(docNum), 'w')
			for content in soup.find_all('p'):
				content = content.get_text()
				content = content.encode('utf-8')
				print(str(content))
				fout.writelines(str(content))
				fout.writelines('\n')
				print("test")
			docNum += 1
			matchtable[currLink] = loop
			for link in soup.find_all('a'):
				href = str(link.get('href')).rstrip("/")
				if 'uic.edu' not in href:
					continue
				if href in visited:
					continue
				if href.startswith('http'):
					size += 1
					q.put(href)
					visited.add(href)
				if href.startswith('/'):
					root = []
					root += currLink.split("://")
					href = root[0] + "://" + root[1].split("/")[0] + href
					if href not in visited:
						size += 1				
						# print(href)
						q.put(href)
						visited.add(href)
			loop += 1
		except:
			pass
	fout = open("output/matchtable.txt", 'w')
	fout.writelines(str(matchtable))
	# print(visited)
	# print(visited)

if __name__ == '__main__':
	scraping()
