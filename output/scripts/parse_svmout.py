"""Parse outputs of classify.py in batch, and summarize results into a csv
file"""

import os, csv

#files that are not plaintext console outputs from classify.py
results  = 'results.csv'
excluded = [os.path.basename(__file__), results]

#prepare output files and write headers
out = open(results, 'w')
w = csv.writer(out, quoting=csv.QUOTE_MINIMAL) #avoid quoting strings in csv
w.writerow(['N-GRAM SIZE', 'N-GRAM TARGET', 'KERNEL', 'VECSIZE', 'C', 'nSV', \
	'SCORE', 'ITERATIONS'])

#parse data from filenames
def readname(filename, start, s):
	stop  = start + filename[start:].find(s)
	return filename[start:stop], stop

#parse data from txtfile
def readtxt(f, n, s0, s1):
	line = f[n]
	n0 = line.find(s0) + len(s0)
	n1 = n0 + line[n0:].find(s1)
	return line[n0:n1]

#start parsing
for filename in os.listdir():
	if filename in excluded: continue #skip file

	with open(filename, 'r') as f:
		f = f.readlines()

		#retrieve common data from filenames
		ngrsize, n = readname(filename, 0, '_')
		target, n = readname(filename, n + 1, '_')
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
