"""Reduces the weight of svm-output plaintext files, by blanking out the lines
full of dots and stars.
Also, it removes the ConvergenceWarning messages that are found in files
created by copy-pasting the text from the console, instead than redirected from
stdout (as it should be), which would otherwise break parse_classifier.py.
"""

import os

#get list of files to shrink
files = os.listdir()
files.remove(os.path.basename(__file__))

#strings to look for
svc  = 'SVC output'
fast = 'Warning: using -h 0 may be faster'
conv = 'ConvergenceWarning'

for filename in files:
	#read & prepare out
	with open(filename, 'r') as f:
		buf = f.readlines()
		for i in range(len(buf)):
			s = buf[i - 1]
			if svc in s or fast in s or conv in s:
				buf[i] = '\n'
			if fast in s or conv in s:
				buf[i - 1] = '\n' #clear the preceding line

		#so far, ConvergenceWarning messages (2 lines) have been blanked
		#out. this would still break parse_classifier.py; so the lines
		#must be physically removed from the file
		for i in range(len(buf)):
			#beware: len(buf) will decrease over time, as the
			#following code will del items from buf. BUT: the range
			#of the for cycle is fixed. the following if statement
			#thus serves as a LBYL check
			if len(buf) > i:
				#recursively delete any blank line
				while 'Total nSV' in buf[i] \
					and 'LibSVM' not in buf[i + 1]:
					del buf[i + 1]

	#write over the same file
	with open(filename, 'w') as out:
		for line in buf:
			out.write(line)
