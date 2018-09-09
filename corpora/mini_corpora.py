#!/usr/bin/env python3

"""Takes a (small) set number of entries from formatted corpora, providing very
	small corpora for testing purposes.
"""

from conf import Corpora

for c in [Corpora.gen, Corpora.inf]:
	with open(c.maxi, 'r') as inp, open(c.mini, 'w') as out:
		inp = inp.readlines()
		for i in range(len(inp)):
			if i< Corpora.minisize:
				out.write(inp[i])
