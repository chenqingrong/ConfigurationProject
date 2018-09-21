import gensim
import os
import smart_open
import random
import collections
import math
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np
def read_corpus(fname,tokens_only=False):
	with smart_open.smart_open(fname,encoding="iso-8859-1") as f:
		for i, line in enumerate(f):
			if tokens_only:
				yield gensim.utils.simple_preprocess(line.split('**')[1])
			else:
				yield gensim.models.doc2vec.TaggedDocument(gensim.utils.simple_preprocess(line.split('**')[1]),[i])

#build and train the models
list_of_file=["apache-configuration","hdfs-configuration","mysql-configuration","php-configuration"]
train_corpus=[]
for f in list_of_file:
	train_corpus+=list(read_corpus(f))
model=gensim.models.doc2vec.Doc2Vec(vector_size=50,min_count=2,epochs=40)
model.build_vocab(train_corpus)
model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)

######testing part 
#read in file
def read_test(fname):
	return open(fname,'r').readlines()
test=[]
for f in list_of_file:
	test+=read_test(f)
for i in range(len(test)):
	test[i]=test[i].split('**')
#assign inferred vectors
scores={}
result={}
error=[]
X=[]
for i in range(len(test)):
	scores[test[i][0]]=model.infer_vector(gensim.utils.simple_preprocess(test[i][1]))
	X.append(scores[test[i][0]])
#k-means
maxkind=15
chosenkind=4
#for i in range(2,maxkind):
#	estimator=KMeans(n_clusters=i)
#	estimator.fit(X)
#	error.append(silhouette_score(X,estimator.labels_,metric='euclidean'))
#x=range(2,maxkind)
#plt.plot(x,error,'o-')
#plt.show()
estimator = KMeans(n_clusters=chosenkind)
estimator.fit(X)
for i in range(chosenkind):
	result[i]=[]
for key in scores.keys():
	tmp=estimator.predict([scores[key]])[0]
	result[tmp].append(key)
f=open('kmeans_result.txt','w')
for key in result.keys():
	f.write(str(key)+' '+str(result[key])+'\n')
f.close()
