#Created by Yumeng Yang on 12/10/2018

import os
import operator
import re
import numpy as np
from scipy.sparse import csc_matrix
import networkx as nx
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import word_tokenize
np.set_printoptions(threshold=np.inf)
def rank(match_index_num, maxth_index_href, graphnode):
	index_num = {}
	index_href = {}
	element = []
	with open(match_index_num, "r", encoding='utf-8') as fin:
		line = fin.readlines()
		element += line[0].split(",")

	element[0] = element[0].strip("\{")
	element[2999] = element[2999].rstrip("}")
	for i in range(0,3000):
		word = []
		element[i] = element[i].strip(" ")
		word += element[i].split(" ")
		word[0] = word[0].strip(":")
		word[1] = word[1].strip("'")
		num = word[0]
		href = word[1]
		index_num[num] = href
		index_href[href] = num
	# print(index_num)
	# print(index_href)

	# buildgraph
	G = np.zeros((3000,30000))
	lines = []
	with open(graphnode, "r", encoding='utf-8') as fin:
		lines += fin.readlines()
		flag = 0
		for i in range(len(lines)):
			if lines[i].startswith("http") and lines[i + 1].startswith("{"):
				lines[i] = lines[i].strip('\n').strip(' ')
				if (lines[i] in index_href.keys()):
					outNum = int(index_href[lines[i]]) - 1
					# print(outNum)
					lines[i + 1] = lines[i + 1].lstrip("{").rstrip("}")
					outto = []
					outto += lines[i + 1].split(",")
					for link in outto:
						link = link.strip(" ").strip("'")
						# print(link)
						if(link in index_href.keys()):
							inNum = int(index_href[link]) - 1
							G[outNum][inNum] = 1

			i+=1
	s = 0.85
	# G = np.array([[0, 1, 1, 0],
	# 			 [0, 0, 1, 0],
	# 			 [1, 1, 1, 0],
	# 			 [0, 1, 1, 1]])
		
	n = G.shape[0]
	before = np.ones(n)
	after = np.zeros(n)
	before[0:] = 1/n
	after[0:] = 0
	while np.sum(np.abs(after-before)) > 0.0001:
		print(np.sum(np.abs(after-before)))
		before = after.copy()
		for i in range(n):
			sum = 0
			for j in range(n):
				if G[j][i] == 1:
					sum = sum + before[j]/np.count_nonzero(G[j])
				# print(np.count_nonzero(G[j]))
			after[i] = (1-s)/n + s * sum
			# print(after[i])
	print(after)
	rank = {}
	for i in range(n):
		rank[i] = after[i]
	sorted_by_value = sorted(rank.items(), key=lambda kv: kv[1], reverse=True)
	print(sorted_by_value)
	# fout = open("../output/finalrank", 'w')
	# fout.writelines(str(sorted_by_value))
	with open("../output/finalrank", 'w') as f:
		for key in range(3000):
			print(sorted_by_value[key])
			f.write(str(sorted_by_value[key]))
			# f.write(str(key))
			
if __name__ == '__main__':
	match_index_num = "../output/match_index_num"
	maxth_index_href = "../output/maxth_index_href"
	graphnode = "../output/graph"

	print(rank(match_index_num,maxth_index_href,graphnode))