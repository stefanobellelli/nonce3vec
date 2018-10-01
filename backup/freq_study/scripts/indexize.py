import sys, pickle
from lib import vecindex

src = 'source_logs/' + sys.argv[1] + '.log'
out = 'partial_indexes/' + sys.argv[1] + '_index.txt'

with open(src, 'r', errors='replace') as f:
	f = f.read().replace('\n', '')
	d = eval(f)
	_, word = vecindex(d, 'word', 50000)
	_, pos = vecindex(d, 'pos', 50000)

with open(out, 'w', errors='replace') as f:
	f.write('WORD:\n' + word + '\nPOS:\n' + pos)
