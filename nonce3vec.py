#!/usr/bin/env python3

"""Runs some or all of the scripts.
Flags:
--corpora         Format corpora
--mini            Generate mini corpora (for testing purposes)
--vectorize       Run vectorizer
--svm --classify  Run SVM classifier
--parse-svm       Parse all SVM output files

--all             Do all of the above

--delete --clean  Delete output files
"""

import os, sys, shutil
from lib import parse_args
from conf import *

def rm(*args):
	for arg in args:
		shutil.rmtree(arg, ignore_errors=True)

#possible argv
c = ['--corpora']
m = ['--mini']
v = ['--vectorize']
s = ['--svm', '--classify']
p = ['--parse']
a = ['--all']
d = ['--delete', '--clean']

#get argv
argv = sys.argv[1:]
if not len(argv): #make --all the default option
	argv += a
if not parse_args(argv, c + m + v + s + p + a + d): #invalid option
	print('Please select a valid option.')

#exec scripts
if parse_args(argv, c + a):
	from scripts import format_bnc, format_wiki
if parse_args(argv, m + a):
	from scripts import mini_corpora
if parse_args(argv, v + a):
	from scripts import vectorize
if parse_args(argv, s + a):
	os.makedirs(Svm.svmdir, exist_ok=True)
	os.system('python3 -u scripts/classify.py > ' + \
		f'{Svm.svmdir}{Svm.desc}.txt')
if parse_args(argv, p + a):
	from scripts import parse

#clean
if parse_args(argv, d):
	rm(Vectors.vecdir, Svm.svmdir, Parser.parserdir)
	corp = Corpora.corpdir
	for f in os.listdir(corp):
		if f.endswith('.txt'):
			os.remove(corp + f)
		if f.startswith('__'):
			shutil.rmtree(corp + f, ignore_errors=True)
	done = True

#delete bytecode
rm('__pycache__', 'scripts/__pycache__')
