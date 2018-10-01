#!/usr/bin/env python3

"""Formats a raw chimera dataset for SVM classification."""

with open('testset_chimeras.txt', 'r') as src:
	src = src.readlines()

out = ''
for i in range(len(src)):
	src[i] = src[i].split('\t')
	src[i][1] = src[i][1].split(' @@ ')
	for s in src[i][1]:
		s = s.replace('___', 'nonce')
		out += f'{src[i][0]} :: {s}\n'

with open('foout', 'w') as f:
	for line in out:
		f.write(line)
