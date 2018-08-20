"""Plot a vector space in 2D"""

from pandas import DataFrame
from matplotlib import cm
from sklearn.manifold import TSNE
from numpy import array

def run_TSNE(mat):
	return array(TSNE(n_components = 2).fit_transform(mat))

def makefigure(src_m2d):#, labels):
	cmap = cm.get_cmap('nipy_spectral')

	m2d = DataFrame(src_m2d)
	m2d.columns = ['tSNE1','tSNE2']
	m2d.head()

	ax = m2d.plot(kind = 'scatter', x = 'tSNE1', y = 'tSNE2', \
		figsize = (30, 18), c = range(len(m2d)), colormap = cmap, \
		linewidth = 0, legend = False)
	ax.set_xlabel('x')
	ax.set_ylabel('y')

	#for i, word in enumerate(m2d.index):
	#	ax.annotate(word, (m2d.iloc[i].PC2, m2d.iloc[i].PC1), \
	#		color = 'black', size = 'large', \
	#		textcoords = 'offset points')

	return ax.get_figure()

import pickle

with open('pickle', 'rb') as f:
	src = pickle.load(f)

srcmat = []
for k, v in src.items():
	srcmat.append(v)
srcmat = np.array(srcmat)

m2d = run_TSNE(srcmat)
fig = makefigure(m2d)
fig.savefig('fig.png')
