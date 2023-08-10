import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn import preprocessing
import matplotlib.pyplot as plt

#https://www.youtube.com/watch?v=Lsue2gEM9D0

class Calculate_PCA:
	def __init__(self, rawdata):

		data = rawdata.dataframe

		for i in data.index:
			data.loc[i] = rawdata.data[i]


		scaled_data = preprocessing.scale(data.T)
		#StandardScaler().fit_transform(data.T)

		pca = PCA()
		pca.fit(scaled_data)
		pca_data = pca.transform(scaled_data)

		per_var = np.round(pca.explained_variance_ratio_* 100, decimals=1)
		labels = ['PC' + str(x) for x in range(1, len(per_var)+1)]

		#plt.bar(x=range(1,len(per_var)+1), height=per_var, tick_label=labels)
		#plt.plot()
		#plt.ylabel('Percentage of Explained Variance')
		#plt.xlabel('Principal Component')
		#plt.title(f'Scree Plot - {rawdata.smartname} Day {rawdata.day} Repeat {rawdata.repeats[0]}')
		#plt.xticks(rotation=45)
		#plt.show()

		pca_df = pd.DataFrame(pca_data, index=rawdata.sensorlabels, columns=labels)

		plt.scatter(pca_df.PC1, pca_df.PC2)
		plt.title(f'PCA Graph - {rawdata.smartname} Day {rawdata.day} Repeat {rawdata.repeats[0]}')
		plt.xlabel('PC1 - {0}%'.format(per_var[0]))
		plt.ylabel('PC2 - {0}%'.format(per_var[1]))

		for sample in pca_df.index:
			plt.annotate(sample, (pca_df.PC1.loc[sample], pca_df.PC2.loc[sample]))

		plt.show()

		loading_scores = pd.Series(pca.components_[0], index=rawdata.timelabels)
		sorted_loading_scores = loading_scores.abs().sort_values(ascending=False)

		top_10_sensors = sorted_loading_scores.iloc[0:10].index.values

		print("Top 10 sensors:") 
		print(loading_scores[top_10_sensors])


class Calculate_PCA_2:
	def __init__(self, data, vp):

		scaled_data = preprocessing.scale(data.T)
		#StandardScaler().fit_transform(data.T)
		pca = PCA()
		pca.fit(scaled_data)
		pca_data = pca.transform(scaled_data)

		per_var = np.round(pca.explained_variance_ratio_* 100, decimals=1)
		labels = ['PC' + str(x) for x in range(1, len(per_var)+1)]

		if False:
			plt.bar(x=range(1,len(per_var)+1), height=per_var, tick_label=labels)
			plt.plot()
			plt.ylabel('Percentage of Explained Variance')
			plt.xlabel('Principal Component')
			plt.title(f'Scree Plot - '+ str(data.pen))
			plt.xticks(rotation=45)
			plt.show()

		pca_df = pd.DataFrame(pca_data, index=list(data.columns.values), columns=labels)

		for i,j in enumerate(pca_df.PC1):
			plt.scatter(pca_df.PC1.values[i], pca_df.PC2.values[i], color= vp.get(pca_df.index[i]))

		foo = data.pen
		plt.title(f'PCA Graph (Descriptor = {data.type})')

		#plt.title(f'PCA Graph - {data.pen} (Descriptor = {data.type})')
		plt.xlabel('PC1 - {0}%'.format(per_var[0]))
		plt.ylabel('PC2 - {0}%'.format(per_var[1]))

		for sample in pca_df.index:
			plt.annotate(sample, (pca_df.PC1.loc[sample], pca_df.PC2.loc[sample]))

		plt.show()

		loading_scores = pd.Series(pca.components_[0], index=list(data.index.values))
		sorted_loading_scores = loading_scores.abs().sort_values(ascending=False)

		top_10_sensors = sorted_loading_scores.iloc[0:10].index.values



if __name__ == '__main__':
	import pickle
	file = open('data/Pen 6A_Day 18_15_15_25.46.data', 'rb')
	data = pickle.load(file)
	file.close()

	Calculate_PCA(data)