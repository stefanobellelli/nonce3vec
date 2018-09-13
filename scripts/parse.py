#!/usr/bin/env python3

"""Parse outputs of classify.py in batch, and summarize results into a csv
file"""

import os, csv
from lib import readname, readtxt
from conf import Svm, Parser

#prepare output files and write headers
os.makedirs(Parser.parserdir, exist_ok=True)
out = open(Parser.parserdir + Parser.results, 'w')
w = csv.writer(out, quoting=csv.QUOTE_MINIMAL) #avoid quoting strings in csv
w.writerow(Parser.headers)

#start parsing
files = [x for x in os.listdir(Svm.svmdir) if x.endswith('.txt')]
for i in range(len(files)):
	files[i] = Svm.svmdir + files[i]

for filename in files:
	with open(filename, 'r') as f:
		f = f.readlines()

		#retrieve common data from filenames
		n = len(Svm.svmdir)
		ngrsize, n = readname(filename, n, '_')
		target,  n = readname(filename, n + 1, '_')
		vecsize, n = readname(filename, n + 1, '.txt')
		vecsize = int(vecsize)

		while True:
			try:
				while 'optimization' not in f[0]:
					f = f[1:]
			except:
				break #reached EOF

			#retrieve data from text
			iterations = int(readtxt(f, 0, '#iter = ', '\n'))
			nsv = int(readtxt(f, 3, 'Total nSV = ', '\n'))
			c = float(readtxt(f, 7, 'C=', ','))
			kernel = readtxt(f, 8, 'kernel=\'', '\'')
			score = float(readtxt(f, 12, 'Score: ', '\n'))

			f = f[13:]

			w.writerow([ngrsize, target, kernel, vecsize, c, nsv, \
				score, iterations])
