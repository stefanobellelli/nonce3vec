with open('parsed_word.csv', 'r') as f:
	f = f.readlines()

out = {}

for line in f:
	line = line.split()
	if line[1] not in out:
		out[line[1]] = 0
	if line[2] == '2':
		out[line[1]] += 1

with open('meta.csv', 'w') as o:
	for key, value in out.items():
		o.write(key + ',' + str(value) + '\n')