# Created by Yumeng Yang on 12/8/2018
# -*- coding: utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup
import ssl
def scraping():
	ssl._create_default_https_context = ssl._create_unverified_context
	init_link = "https://www.uic.edu/"

	page = urllib.request.urlopen(init_link).read()
	soup = BeautifulSoup(page, 'html.parser')
	for link in soup.find_all('p'):
		content = link.string.encode('utf-8')
		print(content)
	for link in soup.find_all('title'):
		print(link.get_text().encode('utf-8'))
	# for link in soup.find_all('a'):
	# 	print(link.encode('utf-8'))
	# print(html)


if __name__ == '__main__':
	scraping()
