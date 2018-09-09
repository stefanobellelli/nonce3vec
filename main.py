#/usr/bin/env python3

"""Runs some or all of the scripts.
Flags:
--corpora         Format corpora
--mini            Generate mini corpora (for testing purposes)
--vectorize       Run vectorizer
--svm --classify  Run SVM classifier
--parse-svm       Parse all SVM output files

--all             Do all
"""

import os, sys
from lib import newdirs, parse_args
from conf import Svm

flags = sys.argv[1:]
doall = ['--all']

#exec scripts
if parse_args(flags, ['--corpora'] + doall):
	from corpora import format_bnc
	from corpora import format_wiki
if parse_args(flags, ['--mini'] + doall):
	from corpora import mini_corpora
if parse_args(flags, ['--vectorize'] + doall):
	from vectorize import vectorize
if parse_args(flags, ['--svm' '--classify'] + doall):
	newdirs(Svm.subdir)
	os.system('python3 -u {Svm.maindir}/classify.py > ' + \
		f'{Svm.subdir}{Svm.desc}.txt')
