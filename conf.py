"""Contains all customizable settings.
Comments document the purpose of each var.
"""

class Corpora: #where raw src corpora and formatted outputs are stored
	## GENERAL ##
	size     = 5000  #max size of formatted corpora
	minisize = 100   #max size for minified formatted corpora
	usemini  = False #feed vectorize.py with mini corpora

	## CORPUS-WISE ##
	class Corpus:
		corpdir  = 'corpora/'
		mini     = '_mini'

		def __init__(self, name, kind, usemini, minioffset):
			# SETTINGS
			self.name       = name
			self.kind       = kind
			self.minioffset = minioffset

			# DIRECTORIES
			s   = self.corpdir + name
			ext = '.txt'
			self.srcdir     = s + '/'
			self.minified   = s + self.mini + ext
			self.formatted  = self.minified if usemini else s + ext

	#generate corpus objects
	gen = Corpus(name = 'bnc',  kind = 'gen', usemini = usemini, \
		minioffset = 0)
	inf = Corpus(name = 'wiki', kind = 'inf', usemini = usemini, \
		minioffset = 0)

class Logs: #where plaintext logfiles are stored
	logdir = 'log/'
	#dictionary of all per-nonce frequencies (the two dicts in one file):
	udict  = logdir + 'unified_dictionary.log'
	#ordered index of vector dimensions:
	uindex = logdir + 'unified_index.log'

	def __init__(self, subdir):
		self.dir      = self.logdir + subdir
		#pos-tagged corpora:
		self.postag   = self.dir + 'tagged.log'
		#dict of per-nonce (relative) frequencies:
		self.dic      = self.dir + 'dictionary.log'
		#vectors of pos n-grams dimensions:
		self.posvec   = self.dir + 'posvec.log'
		#vectors of word n-grams dimensions:
		self.wordvec  = self.dir + 'wordvec.log'

class Vectors: #where pickled (binary) vector-space files are stored
	## SETTINGS ##
	ngrsize = 2         #size of n-grams (stay below 5 to avoid errors!)
	vecsize = 1000      #cut to n most frequent n-grams
	exclude = []        #uncomment following line to exclude lised n-grams
	if False:           #exclude certain n-grams (switch to True)
		exclude = ['is_a', 'is_an', 'is_the', 'VBZ_DT']

	## DIRECTORIES ##
	vecdir = 'vec/'

	def __init__(self, subdir):
		self.dir     = self.vecdir + subdir
		self.wordvec = self.dir + 'wordvec.pickle'
		self.posvec  = self.dir + 'posvec.pickle'

class Svm: #where SVM plotted graphs are stored
	## SETTINGS ##
	#training
	target     = 'word' #'word' or 'pos'
	C          = [10**exp for exp in range(-1, 5)]
	                    #logscale of values to calc by classifier.py
	kernel     = ['linear', 'rbf', 'poly']
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

	## DIRECTORIES ##
	svmdir = 'svm/'
	nonorm  = svmdir + 'confusion.png'
	yesnorm = svmdir + 'confusion-norm.png'
