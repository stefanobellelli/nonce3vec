#!/usr/bin/env python3

"""Contains functions called by other files."""

import os, numpy as np, json, random, spacy
from itertools import product
from matplotlib import pyplot as plt
from random import shuffle
from sklearn.metrics import confusion_matrix

def parse_args(given, control):
	"""checks if some of the given args are valid for a condition"""
	pairs =  [(x, y) for x in given for y in control]
	for g, c in pairs:
		if g == c:
			return True
	return False

def badtoken(t):
	"""check if t is punctuation, space, or newline char"""
	return t.is_punct or t.text in [' ', '\n'] #or t.tag_ == 'CD'

def removepunct(string, nlp):
	"""remove punctuation from string"""
	out = ''

	for token in nlp(string.rstrip()):
		if badtoken(token): continue
		out += token.text + ' '

	out = out[:-1] #remove trailing space
	return out

def getnonce(string, previous):
	"""pick a random word in a line as nonce"""

	#pick a word as nonce, and keep trying until an unused one is picked
	for i in range(10):
		out = random.choice(string.split()) #random-pick word
		if out not in previous: break #success: exit loop
		out = False #invalid nonce is turned into bool (error msg)

	return out

def getcontext_gen(rng, corpus, nums, nonces, nlp):
	"""pick a line from src corpus, pair with nonce, and output"""
	#infinite loop with strategic continue/break points
	while True:
		#choose line
		n = random.choice(rng) #random-pick a line number
		if n in nums: continue #discard if already picked

		#get a line >= 3 words (excluding punctuation)
		line = corpus[n]
		nopunct = removepunct(line, nlp)
		if len(nopunct.split()) < 3: continue #discard and retry

		#get nonce not already picked for another sentence
		nonce = getnonce(nopunct, nonces)
		if type(nonce) is not str: continue
			#if getnonce() has failed (after 10 attempts) at picking
			#a new nonce, then getcontext_gen() proceeds to pick a
			#new line

		break #everything's ok if this point is reached

	#remove initial space
	if line[0] is ' ':
		line = line[1:]

	return n, line, nonce

def getline_inf(rng, corpus, nums):
	"""pick a line from src corpus, pair with nonce, and output"""
	#infinite loop with strategic continue/break points
	while True:
		#choose line
		n = random.choice(rng) #random-pick a line number
		if n in nums: continue #discard if already picked

		#get a line >= 3 words (avoid 'word .')
		line = corpus[n]
		if len(line.split()) < 3: continue
			#if line is < 3 words, retry from start (pick new line)

		break #everything's ok if this point is reached

	return n, line

def sanitize(string):
	"""remove quirks of corpora (especially wiki)"""
	#convert strange space chars to standard 0x20
	string = string.replace(chr(0xA0), ' ').replace(chr(0x2009), ' ')
	#recursively remove multiple spaces
	while '  ' in string: string = string.replace('  ', ' ')

	return string

def postag(src):
	"""pos-tag an external file"""
	nlp = spacy.load('en')
	log  = '' #for logfile
	out  = {} #for later processing

	for line in src:
		#split nonce and context
		n        = line.find('::')
		nonce    = line[:n - 1]
		context  = line[n + 3:]

		#add pos-tagged src line to output and logfile
		out[nonce] = []
			#format: {nonce : [[token, tag], [token, tag], ...]}
		logline = nonce + ' ::'
			#format: 'nonce :: token_tag, token_tag, ...'

		for token in nlp(context):
			if badtoken(token): continue #discard token
			out[nonce].append([token.text, token.tag_])
			logline += ' ' + token.text + '_' + token.tag_
		log += logline + '\n'

	return out, log

def ngrams(line, size, blacklist):
	"""list all n-grams, and exclude from blacklist"""
	out = [] #format: [AA_BB, CC_DD, ...]

	for i in range(len(line) - size + 1):
		#get one n-gram
		buf = ''
		for j in range(size):
			buf += line[i+j] + '_'
		buf = buf[:-1] #remove trailing underscore

		if buf not in blacklist:
			out.append(buf)

	return out

def add_to_dic(dic, key):
	"""increment +1 val of dic[key] if present, else set dic[key] = 1"""
	if key in dic:
		return dic[key] + 1
	return 1

def dictize(dic, size, blacklist):
	"""create a dictionary of word & pos n-grams (of chosen size) for each
	nonce
	"""
	out = {}

	for nonce in dic:
		#init sub-dict
		out[nonce]         = {}
		out[nonce]['word'] = {}
		out[nonce]['pos']  = {}

		#create lists of just words and just pos
		word = [i[0] for i in dic[nonce]]
		pos  = [i[1] for i in dic[nonce]]

		#create lists of ngrams of words and pos
		ngr_word = ngrams(word, size, blacklist)
		ngr_pos  = ngrams(pos, size, blacklist)

		#create/update dictionary of ngrams for each nonce
		for i in range(len(ngr_word)):
			out[nonce]['word'][ngr_word[i]] = \
				add_to_dic(out[nonce]['word'], ngr_word[i])
		for i in range(len(ngr_pos)):
			out[nonce]['pos'][ngr_pos[i]] = \
				add_to_dic(out[nonce]['pos'], ngr_pos[i])
	
	log = json.dumps(out, indent = 4) #prepare log
	return out, log

def vecindex(dic, string, size):
	"""incrementally list all ngrams of a given type in a dictionary"""
	# list of all word-wise [n-gram, freq] pairs
	buf = []
	for nonce in dic:
		for key, value in dic[nonce][string].items():
			buf.append([key, value])

	#cumulate word-wise freqs into absolute freq
	out = []

	for lst in buf:
		ngr = lst[0] #get n-gram
		outngr = [sublist[0] for sublist in out]
			#get all n-grams already appended to out

		#if n-gram already appended: increment abs freq += rel freq
		#else: add [n-gram, rel freq]
		if ngr not in outngr:
			out.append(lst)
		else:
			i = outngr.index(ngr)
			out[i][1] += lst[1]

	#shuffle order of pairs (to avoid first-in-first-out bias)
	shuffle(out)
	#sort descending by freq, and cut to size
	out = sorted(out, key = lambda x : x[1], reverse = True)[:size]

	#create log
	log = ''
	for lst in out:
		log += f'{lst[0]} {lst[1]}\n'

	#create output
	out = [i[0] for i in out]

	return out, log

def unifiedindex(size, *args):
	"""make unified index of all n-grams
	(from list of dictionaries of type nonce:set_of_n-grams)
	"""
	w = 'word'
	p = 'pos'

	#populate unified dict of all {nonce: set_of_n-grams}
	udict = {}
	for ngrdict in args: #should be 2 args: just join the 2 dicts
		udict.update(ngrdict)
	udictlog = json.dumps(udict, indent=4) #prepare log

	#create cross-nonce indexes of all n-grams
	#(dividing between words and pos)
	wordindex, wlog = vecindex(udict, w, size)
	posindex,  plog = vecindex(udict, p, size)
	#prepare log
	uindexlog = f'{w.upper()}:\n' + wlog + '\n' + f'{p.upper()}:\n' + plog

	return wordindex, posindex, udictlog, uindexlog

def make_vec_log(dic):
	"""render ngram vectors, stored in a dictionary by vectorize(), in a
	readable form
	"""
	#find longest nonce (value needed later)
	maxlen = 0
	for nonce in dic:
		n = len(nonce)
		if n > maxlen: maxlen = n

	out = ''
	for nonce in dic:
		#align vectors to longest nonce
		s = nonce
		while len(s) < maxlen: s += ' '
		out += s

		#append vector values
		for val in dic[nonce]:
			out += ' ' + str(val)

		out += '\n'
	return out

def vectorize(dic, index, switch):
	"""create vectors of ngrams of a given type for all nonces in a
	dictionary (vectors are stored as values of a dictionary where each
	nonce is a key).
	index = freq-sorted list of all n-grams; switch = 'word' or 'pos'.
	"""
	n = len(index) #no. of n-grams
	out = {}

	for nonce in dic:
		vec = [0] * n #prealloc list of ints as 0's
		context = dic[nonce][switch]

		#get each n-gram in index: if present in line,
		#add to vec the rel freq of n-gram in line (else stays == 0)
		for i in range(n):
			ngram = index[i]
			if ngram in context:
				vec[i] = context[ngram]

		out[nonce] = vec

	log = make_vec_log(out)

	return out, log

def make_arrays(space, n):
	"""create numpy arrays of all nonces and vectors for SVM train and test.
	first n entries of vector space go to train, others to test.
	"""
	trainnonces = []
	testnonces  = []
	trainvec    = []
	testvec     = []

	i = 0

	for key, value in space.items():
		if i < n:
			trainnonces.append(key)
			trainvec.append(value)
			i += 1
		else:
			testnonces.append(key)
			testvec.append(value)
	return np.array(trainvec), np.array(testvec), trainnonces, testnonces, \
		len(testvec) #no need for trainvec, since it's == n

def make_labels(size1, size2):
	"""labels for y-axis of train/test (used by SVM)"""
	out = []
	for i in range(size1):
		out.append(1)
	for i in range(size2):
		out.append(2)
	return np.array(out)

def normalize(vec):
	"""calc normalized vector"""
	norm = np.linalg.norm(vec)
	if norm == 0:
		return vec 
	return vec / norm

def get_queries(f):
	"""create dict = {nonce: vector, nonce: vector, ...} for real-queries
	txt file
	(DEPRECATED: waiting for actual format of the file!))"""
	out = {}
	with open(f, 'r') as f:
		lines = f.readlines()

	for line in lines:
		line  = line.rstrip().split('::')
		nonce = line[0]
		vec   = normalize(np.array([float(i) \
			for i in line[1].split()]))
		out[nonce] = vec

	return out

def plot_confmat(mat, classes, title, normalized):

	handle = plt.figure()

	plt.imshow(mat, interpolation='nearest', cmap=plt.cm.Blues)
	plt.title(title)
	plt.colorbar()
	tick_marks = np.arange(len(classes))
	plt.xticks(tick_marks, classes, rotation=45)
	plt.yticks(tick_marks, classes)

	fmt = '.2f' if normalized else 'd'
	threshold = mat.max() / 2
	for i, j in product(range(mat.shape[0]), range(mat.shape[1])):
		plt.text(j, i, format(mat[i, j], fmt),
		horizontalalignment='center', \
                color='white' if mat[i, j] > threshold else 'black')

	plt.tight_layout()
	plt.ylabel('True label')
	plt.xlabel('Predicted label')

	return handle

def make_confmat(y_test, y_pred, t1, t2):
	"""Computes confusion matrices, then passes them as both str and fig
	to the calling script.
	"""

	#objs to pass to main script
	class Confmat:
		def __init__(self, mat, title):
			self.title = title
			self.mat   = mat
			self.str   = f'{title}:\n{str(mat)}\n'
			self.img   = plot_confmat(mat, [t1, t2], title, True)

	#flush open figures
	plt.close('all')

	#confmat (no normalization)
	title = 'Confusion matrix, without normalization'
	mat   = confusion_matrix(y_test, y_pred) #compute confmat
	nonorm = Confmat(mat, title)

	#confmat (normalized)
	title = 'Normalized confusion matrix'
	mat = mat.astype('float') / mat.sum(axis=1)[:, np.newaxis] #normalize
	np.set_printoptions(precision=2) #set precision for str output
	yesnorm = Confmat(mat, title)

	return nonorm, yesnorm

def readname(filename, start, s):
	"""Parses data from filenames."""
	stop  = start + filename[start:].find(s)
	return filename[start:stop], stop

def readtxt(f, n, s0, s1):
	"""Parses data from plaintext files."""
	line = f[n]
	n0 = line.find(s0) + len(s0)
	n1 = n0 + line[n0:].find(s1)
	return line[n0:n1]
