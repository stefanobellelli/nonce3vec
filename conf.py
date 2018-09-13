#!/usr/bin/env python3

"""Contains all customizable settings.
Comments document the purpose of each var.
"""

class Corpora: #where raw src corpora and formatted outputs are stored

	## GENERAL ##
	size     = 5000  #max size of formatted corpora
	minisize = 100   #max size for minified formatted corpora
	usemini  = False #feed vectorize.py with mini corpora

	corpdir  = 'corpora/'

	## CORPUS-WISE ##
	class Corpus:
		def __init__(self, corpdir, name, kind, usemini):
			self.kind = kind

			# DIRECTORIES
			s = corpdir + name
			ext = '.txt'

			self.srcdir = s + '/'
			self.maxi = f'{s}{ext}'
			self.mini = f'{s}_mini{ext}'
			self.formatted = self.mini if usemini else self.maxi

	#generate corpus objects
	gen = Corpus(corpdir, 'bnc',  'gen', usemini)
	inf = Corpus(corpdir, 'wiki', 'inf', usemini)

class Vectors: #where pickled (binary) vector-space files are stored

	## SETTINGS ##

	ngrsize = 2         #size of n-grams (stay below 5 to avoid errors!)
	vecsize = 1000      #cut to n most frequent n-grams
	exclude = []        #uncomment following line to exclude lised n-grams
	if False:           #exclude certain n-grams (switch to True)
		exclude = ['is_a', 'is_an', 'is_the', 'VBZ_DT']

	## DIRS & FILES ##
	vecdir = 'vectorize/'
	def __init__(self, subdir):
		
		self.dir = self.vecdir + subdir
		self.wordvec = self.dir + 'wordvec.pickle'
		self.posvec  = self.dir + 'posvec.pickle'

		class Logs:
			def __init__(self, vecdir, subdir):
				#GENERAL LOGS
				self.dir = vecdir + 'logs/'
				#dictionary of all per-nonce frequencies
				#(the two dicts in one file):
				self.udict  = self.dir + \
					'unified_dictionary.log'
				#ordered index of vector dimensions:
				self.uindex = self.dir + 'unified_index.log'

				#TOPICWISE LOGS
				self.dir += subdir
				#pos-tagged corpora:
				self.postag  = self.dir + 'tagged.log'
				#dict of per-nonce (relative) frequencies:
				self.dic     = self.dir + 'dictionary.log'
				#vectors of pos n-grams dimensions:
				self.posvec  = self.dir + 'posvec.log'
				#vectors of word n-grams dimensions:
				self.wordvec = self.dir + 'wordvec.log'

		self.logs = Logs(self.vecdir, subdir)

class Svm: #where SVM plotted graphs are stored

	## SETTINGS ##

	#training
	target     = 'pos' #'word' or 'pos'
	C          = [1]#[10**exp for exp in range(-1, 5)]
	                    #logscale of values to calc by classifier.py
	kernel     = ['linear']
	                    #kernels to be used
	degree     = 3      #relevant for 'poly' only
	shownonces = False  #print training nonces
	trainsize  = 3500   #SVM training lines per condition (tot is twice)
	maxiter    = 10**7  #timeout after this

	#plotting
	plot       = True   #save confmat in .png file

	#testing
	realtest  = False   #test on real queries (not implemented!)
	queryfile = 'queryvec.txt' #file with real queries

	## DIRS & FILES ##

	desc    = f'{Vectors.ngrsize}_{target}_{Vectors.vecsize}'
	nonorm  = 'confmat.png'
	yesnorm = 'conf-norm.png'	

	svmdir = 'classify/'
	pngdir  = f'{svmdir}{desc}/'

class Parser:

	## SETTINGS ##

	headers = ['N-GRAM SIZE', 'N-GRAM TARGET', 'KERNEL', 'VECSIZE', 'C', \
		'nSV', 'SCORE', 'ITERATIONS']

	## DIRS & FILES ##
	results = Svm.desc + '_results.csv'
	parserdir = 'parse/'
