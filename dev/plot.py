"""Plot a vector space in 2D"""

import pickle
from pandas import DataFrame
from sklearn.manifold import TSNE
import numpy as np

def get_dataframe(filename):
	#access dict
	with open(filename, 'rb') as f:
		dic = pickle.load(f)

	#create matrix of vectors
	mat = []
	for k, v in dic.items():
		mat.append(v)
	mat = np.array(mat)

	#run tsne
	mat = TSNE(n_components = 2).fit_transform(mat)

	#create dataframe
	dataframe = DataFrame(mat)
	dataframe.columns = ['tSNE1', 'tSNE2']
	dataframe.head()

	return dataframe

#calc dataframes
gen_df = get_dataframe('posvec_gen.pickle')
inf_df = get_dataframe('posvec_inf.pickle')

ax = gen_df.reset_index().plot(kind = 'scatter', x = 'tSNE1', y = 'tSNE2', \
		figsize = (30, 18), color = 'red', label = 'G1')
inf_df.reset_index().plot(kind = 'scatter', x = 'tSNE1', y = 'tSNE2', \
		figsize = (30, 18), color = 'blue', label = 'G2', ax = ax)

fig = ax.get_figure()
fig.savefig('fig.png')
