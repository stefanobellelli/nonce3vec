import sys,csv

def loadindex(f):
	with open(f, 'r') as f:
		tbdel = []
		out = f.read().split('\n')
		for i in range(len(out)):
			if ' ' not in out[i]:
				tbdel.append(i)
				continue
			out[i] = out[i].split()
			out[i][1] = int(out[i][1])
		tbdel.sort(reverse=True)
		for i in tbdel:
			del out[i]
	return out

uni = loadindex('unified_indexes/' + sys.argv[1] + '_unified_index.log')
gen = loadindex('partial_indexes/' + sys.argv[1] + '_gen_index.txt')
inf = loadindex('partial_indexes/' + sys.argv[1] + '_inf_index.txt')

out = uni
for i in range(len(out)):
	out[i] += (0, 0)

for i in range(len(out)):
	for j in range(len(gen)):
		if out[i][0] == gen[j][0]:
			out[i][2] = gen[j][1]
	for j in range(len(inf)):
		if out[i][0] == inf[j][0]:
			out[i][3] = inf[j][1]

with open('freqlists/' + sys.argv[1] + '_results.csv', 'w') as f:
	w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
	w.writerow(['N-GRAM', 'TOT', 'GEN', 'INF'])
	for i in range(len(out)):
		w.writerow(out[i])
