#Create by Yumeng Yang on 12/10/2018

import os
import operator

# ----- GLOBAL VARIABLES -----
word_dict = {}
word_in_doc = {}
word_freq_in_doc = {}
max_freq_in_doc = {}
Q_word_dict = {}
Q_word_in_doc = {}
Q_word_freq_in_doc = {}
Q_max_freq_in_doc = {}
#------------------------------

def indexDoc(src, out):

# ----- GLOBAL VARIABLES -----
	global word_dict
	global word_in_doc
	global word_freq_in_doc
	global max_freq_in_doc
#------------------------------
	
	files = os.listdir(src)
	DocNum = 0
	for file in files:
		with open(src + "/" + file, "r", encoding='utf-8') as f:
			word_freq_in_doc[file] = {}
			lines = f.readlines()
			for line in lines:
				line = line.strip('\n')
				words = []
				words += line.split(' ')
				for word in words:
					if word == '':
						continue
					if word not in word_freq_in_doc[file]:
						word_freq_in_doc[file][word] = 1
					else:
						word_freq_in_doc[file][word] += 1
					if word not in word_dict: 
						word_dict[word] = 1
						word_in_doc[word] = {}
						word_in_doc[word][file] = 1
					else:
						word_dict[word] += 1						
						if file not in word_in_doc[word]:
							word_in_doc[word][file] = 1
						else:
							word_in_doc[word][file] += 1

	# print(word_in_doc)
	for doc in word_freq_in_doc:
		biggest = 0
		for term in word_freq_in_doc[doc]:
			if word_freq_in_doc[doc][term] > biggest:
				biggest = word_freq_in_doc[doc][term]
		max_freq_in_doc[doc] = biggest
	with open(out + "/word_dict.txt", 'w') as f:
		f.write(str(word_dict))
	with open(out + "/word_in_doc.txt", 'w') as f:
		f.write(str(word_in_doc))
	with open(out + "/word_freq_in_doc.txt", 'w') as f:
		f.write(str(word_freq_in_doc))
	with open(out + "/max_freq_in_doc.txt", 'w') as f:
		f.write(str(max_freq_in_doc))

def processQuery(query):
	import re
	from nltk.stem import PorterStemmer
	from nltk.tokenize import sent_tokenize, word_tokenize
	from nltk import word_tokenize
	from nltk.corpus import stopwords

	stop = set(stopwords.words('english'))
	ps = PorterStemmer()
	punctuations = '''!()-[]{},;:'"\,`<>./?@#$%^&*_~'''

	global Q_word_dict
	global Q_word_in_doc
	global Q_word_freq_in_doc
	global Q_max_freq_in_doc
	DocNum = 0
	words = []
	result = []
	words += re.split(' ',query)
	for word in words:
		if word in punctuations:
			continue;
		if word.lower() in stop: 
			continue;
		newword = ps.stem(word.lower())
		print(newword)
		newword = re.sub("[0-9/=()><;\\\[\]\{\}|?$&!:,']", " ", newword)
		if len(newword) < 2:
			continue;
		if newword in stop:
			continue;
		result.append(newword)
		result.append(' ')
	print(result)
	fout = open("../output/search/" + "query", 'w')
	fout.writelines(result)



def indexQuery(src, out):
	files = os.listdir(src)
	global Q_word_dict
	global Q_word_in_doc
	global Q_word_freq_in_doc
	global Q_max_freq_in_doc
	DocNum = 0
	for file in files:
		with open(src + "/" + file, "r", encoding='utf-8') as f:
			Q_word_freq_in_doc[file] = {}
			lines = f.readlines()
			for line in lines:
				line = line.strip('\n')
				words = []
				words += line.split(' ')
				for word in words:
					if word == '':
						continue
					if word not in Q_word_freq_in_doc[file]:
						Q_word_freq_in_doc[file][word] = 1
					else:
						Q_word_freq_in_doc[file][word] += 1
					if word not in Q_word_dict: 
						Q_word_dict[word] = 1
						Q_word_in_doc[word] = {}
						Q_word_in_doc[word][file] = 1
					else:
						Q_word_dict[word] += 1						
						if file not in Q_word_in_doc[word]:
							Q_word_in_doc[word][file] = 1
						else:
							Q_word_in_doc[word][file] += 1
	for doc in Q_word_freq_in_doc:
		biggest = 0
		for term in Q_word_freq_in_doc[doc]:
			if Q_word_freq_in_doc[doc][term] > biggest:
				biggest = Q_word_freq_in_doc[doc][term]
		Q_max_freq_in_doc[doc] = biggest
	with open(out + "/Q_word_dict.txt", 'w') as f:
		f.write(str(Q_word_dict))
	with open(out + "/Q_word_in_doc.txt", 'w') as f:
		f.write(str(Q_word_in_doc))
	with open(out + "/Q_word_freq_in_doc.txt", 'w') as f:
		f.write(str(Q_word_freq_in_doc))
	with open(out + "/Q_max_freq_in_doc.txt", 'w') as f:
		f.write(str(Q_max_freq_in_doc))

def Retrieval(src):
	from collections import defaultdict
	import math
	import cmath

# ----------GLOBAL VARIABLES-------------
	global Q_word_dict
	global Q_word_in_doc
	global Q_word_freq_in_doc
	global Q_max_freq_in_doc
	global word_dict
	global word_in_doc
	global word_freq_in_doc
	global max_freq_in_doc
# ---------------------------------------

	files = os.listdir(src)
	Cos = defaultdict(defaultdict)
	for file in files:
		with open(src + "/" + file, "r", encoding='utf-8') as f:
			Qwij = {}
			Dwij = defaultdict(defaultdict)
			lines = f.readlines()
			for line in lines:
				line = line.strip('\n')
				words = []
				words += line.split(' ')
				for word in words:
					if word == '':
						continue
					Qtfij = Q_word_freq_in_doc[file][word]/Q_max_freq_in_doc[file]
					if word in word_in_doc:
						Qidfi = math.log2(len(max_freq_in_doc)/len(word_in_doc[word]))
					else:
						Qidfi = 0
					Qwij[word] = Qtfij * Qidfi

					for doc in word_freq_in_doc:
						if word in word_freq_in_doc[doc]:
							Dtfij = word_freq_in_doc[doc][word]/max_freq_in_doc[doc]
							Didfi = math.log2(len(max_freq_in_doc)/len(word_in_doc[word]))
						else:
							# print(file + " " + doc + " " + word)
							Dtfij = 0
							Didfi = 0
						Dwij[doc][word] = Dtfij * Didfi
# here!!!!!!!!!!!!!!!!!!!1move this definition inside the loop for doc in Dwij!!!!!!!!!!!!!!!!1
		
		for doc in Dwij:
			up = 0
			down1 = 0
			down2 = 0
			for word in Qwij:
				up = Qwij[word] * Dwij[doc][word] + up
				down1 = Qwij[word] * Qwij[word] + down1
				down2 = Dwij[doc][word] * Dwij[doc][word] + down2
			if down1 * down2 == 0:
				Cos[file][doc] = 0
			else:
				Cos[file][doc] = up/(down1 * down2)**0.5
	for file in Cos:
		ranking = {}
		for doc in Cos[file]:
			ranking[doc] = Cos[file][doc]
		sorted_by_value = sorted(ranking.items(), key=lambda kv: kv[1], reverse=True)

		# get match_index_num
		index_num = {}
		element = []
		with open("../output/match_index_num", "r", encoding='utf-8') as fin:
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

		# get pagerank
		li = []	
		with open("../output/finalrank", 'r') as f:
			arr = []
			line = f.readlines()
			arr += line[0].split(")")
			for i in range(len(arr)):
				li.append(arr[i].split(",")[0].lstrip("("))

		# result
		with open("../output" + file, 'a') as f:				
			by_pagerank = {}
			print("----------------------------")
			for key in range(0, 100):
				docnum = str(sorted_by_value[key]).split(",")[0].lstrip("('").rstrip("'")
				docnum = int(docnum) + 1
				href = index_num[str(docnum)]
				# print(docnum)
				print(href)
				f.write(str(sorted_by_value[key]))
				f.write(str(key))
			# *************************************** #
				docnum = docnum - 1
				pagerank = li.index(str(docnum))
				by_pagerank[docnum] = pagerank
			print("-----------pagerank----------")
			sorted_by_pagerank = sorted(by_pagerank.items(), key=lambda kv: kv[1], reverse=False)
			for key in range(100):
				docnum = str(sorted_by_pagerank[key]).split(",")[0].lstrip("(")
				docnum = int(docnum) + 1
				href = index_num[str(docnum)]
				# print(docnum)
				print(href)
			# **************************************8
			

if __name__ == '__main__':
	preprocessed_doc = '../output/preprocessed1'
	index_doc = '../output/index_doc'
	index_query = '../output/index_query'
	query = "career fair"
	querysrc = "../output/search"	
	# processQuery(query)
	indexDoc(preprocessed_doc, index_doc)
	indexQuery(querysrc, index_query)
	Retrieval(querysrc)
