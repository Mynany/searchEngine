# Created by Yumeng Yang on 12/8/2018
# -*- coding: utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import ssl
import queue
import random
import os

def scraping():
	
	ssl._create_default_https_context = ssl._create_unverified_context
	init_link = "https://www.uic.edu/"

	ua = UserAgent()
	headers = {'User-Agent':ua.random}
	print(headers)
	q = queue.LifoQueue(1000)
	q.put(init_link)
	visited = set()
	loop = 10
	size = 0
	docNum = 0
	while q.qsize() > 0 or len(visited) > 3000:
		print(loop)
		currLink = q.get()
		try:
			urlopen(currLink)
		except:
			pass
		page = urllib.request.urlopen(currLink).read()
		soup = BeautifulSoup(page,'html.parser')
		fout = open("output/" + str(docNum), 'w')
		for content in soup.find_all('p','title','a','link'):
			content = content.get_text()
			content = content.encode('utf-8')
			fout.writelines(str(content))
			fout.writelines('\n')

		docNum += 1
		for link in soup.find_all('a'):
			href = str(link.get('href')).rstrip("/")
			if 'uic' not in href:
				continue
			if href in visited:
				continue
			if href.startswith('http'):
				size += 1
				q.put(href)
				visited.add(href)
				print(href)
			if href.startswith('/'):
				root = []
				root += currLink.split("://")
				href = root[0] + "://" + root[1].split("/")[0] + href
				if href not in visited:
					size += 1				
					print(href)
					q.put(href)
					visited.add(href)
		

		loop -= 1
	print(len(visited))
	# print(visited)
	# print(visited)

if __name__ == '__main__':
	scraping()
