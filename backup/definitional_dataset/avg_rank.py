import sys, statistics

with open(sys.argv[1] + '_out.txt', 'r') as f:
	src = f.readlines()

ranks = []
for i in range(len(src) + 1):
	try:
		if src[i + 1].startswith('--') or src[i + 1].startswith('Final MRR:'):
			ranks.append(int(src[i].split()[0]))
	except:
		pass
ranks.sort()

avgrank = sum(ranks) / len(ranks)
median = statistics.median(ranks)

ci95  = len(ranks) // 40
r95   = ranks[ci95 : -ci95]
avg95 = sum(r95) / len(r95)

ci90  = len(ranks) // 20
r90   = ranks[ci90 : -ci90]
avg90 = sum(r90) / len(r90)

ci80  = len(ranks) // 10
r80   = ranks[ci80 : -ci80]
avg80 = sum(r80) / len(r80)

print(f'avg: {avgrank} - 95ci: {avg95} - 90ci: {avg90} - 80ci: {avg80} - median: {median}')

#wiki = 8112.892596747056
#bnc  = 47793.7142560266