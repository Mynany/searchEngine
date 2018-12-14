#Created by Yumeng Yang on 12/10/2018

import os
import operator
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import word_tokenize
from nltk.corpus import stopwords

stop = set(stopwords.words('english'))
ps = PorterStemmer()

def preprocess(src, output): 
	files = os.listdir(src)
	for file in files:
		if not file.startswith('.'):
			print("processing file" + file)
			result = []
			with open(src + "/" + file, "r", encoding='utf-8') as fin:
				punctuations = '''!()-[]{},;:'"\,`<>./?@#$%^&*_~'''
				lines = fin.readlines()
				for line in lines:
					words = []
					line = line.strip("'").strip(' ').strip('b')
					line = line.strip('\n').strip(' ')
					words += re.split('[,_@&-\.]+',line)
					strp = ''
					for word in words: 
						if word in punctuations:
							continue;
						word = word.strip('\n').strip('"')
						if r'\x' in word:
							continue
						newword = re.sub(r'[^\x00-\x7F]+',' ', word)
						newword = re.sub(r'\n', " ", newword)
						newword = re.sub(r'\r', " ", newword)
						newword = re.sub(r'\t', " ", newword)
						newword = re.sub("[0-9/=()><;\\\[\]\{\}|?$&!:,']", " ", newword)

						# newword = re.sub("[-@]", " ", currword)
						# newword = newword.split(r'\\x')[1]
						
						# if newword.lower() in stop: 
						# 	continue;
						# newword = ps.stem(newword.lower())
						# if len(newword) < 3:
						# 	continue;
						# if newword in stop:
						# 	continue;
						strp = ''.join(newword)
						# print(newword)
						result.append(strp)
						result.append(' ')
			# print(result)
			fout = open(output + file, 'w')
			fout.writelines(result)

	
def preprocess1(src, output):
	files1 = os.listdir(src)
	for file in files1:
		if not file.startswith('.'):
			print("processing1 file" + file)
			result = []
			with open(src + "/" + file, "r", encoding='utf-8') as fin:
				punctuations = '''!()-[]{},;:'"\,`<>./?@#$%^&*_~'''
				lines = fin.readlines()
				for line in lines:
					words = []
					words += re.split(' ',line)
					strp = ''
					for word in words: 
						if word.lower() in stop: 
							continue;
						newword = ps.stem(word.lower())
						if len(newword) < 2:
							continue;
						if newword in stop:
							continue;
						strp = ''.join(newword)
						# print(newword)
						result.append(strp)
						result.append(' ')
			# print(result)
			fout = open(output + file, 'w')
			fout.writelines(result)
if __name__ == '__main__':
	src = '../output/pages'
	output = '../output/preprocessed/'
	output1 = '../output/preprocessed1/'
	preprocess(src, output)
	preprocess1(output, output1)
