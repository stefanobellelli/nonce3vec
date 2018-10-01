import sys
ngrtype = sys.argv[1]

with open('chimeras_' + ngrtype + '.txt', 'r') as f:
	f = f.readlines()

size = ''
out = ''

for line in f:
	if ngrtype.upper() in line:
		size = line[len(ngrtype) + 1:].rstrip()
	if '[1]' in line or '[2]' in line:
		out += size + ' ' + \
			line.split()[0].split('-')[0] + ' ' + \
			line.split()[1].replace('[', '').replace(']', '') + \
			'\n'

with open('parserout.csv', 'w') as o:
	o.write(out)
