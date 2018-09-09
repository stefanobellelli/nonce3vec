#!/usr/bin/env python3

"""Takes a (smalle) set number of entries from corpora, for testing purposes.
"""

from conf import Corpora

for src in [Corpora.gen, Corpora.inf]:
	inp    = src.formatted  #input filename
	out    = src.minified   #output filename
	offset = src.minioffset #no. to lines to discard from beginning

	#print sentences in output file
	with open(inp, 'r') as inp, open(out, 'w') as out:
		inp = inp.readlines()
		for i in range(len(inp)):
			if i>= offset and i < offset + Corpora.minisize:
				out.write(inp[i])
