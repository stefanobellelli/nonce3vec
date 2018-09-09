#/usr/bin/env python3

"""Runs some or all of the scripts.
Flags:
-c --corpora       Format corpora
-m --mini          Generate mini corpora (for testing purposes)
-v --vectorize     Run vectorizer
-s --svm           Run SVM classifier
-p --parse-svm     Parse all SVM output files

-a --all           Do all
"""

import os, sys
from lib import newdirs, parse_args
from conf import Vectors, Svm

flags = sys.argv[1:]
doall = ['-a', '--all']

#exec scripts
if parse_args(flags, ['-c', '--corpora'] + doall):
	import format_bnc
	import format_wiki
if parse_args(flags, ['-m', '--mini'] + doall):
	import mini_corpora.py
if parse_args(flags, ['-v', '--vectorize'] + doall):
	import vectorize
if parse_args(flags, ['-s', '--svm'] + doall):
	newdirs(Svm.svmdir)
	os.system('python3 -u classify.py > ' + \
		f'{Svm.svmdir}{Vectors.ngrsize}_{Svm.target}_{Vectors.vecsize}.txt')
