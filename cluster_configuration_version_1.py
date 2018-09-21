import gensim
import os
import smart_open
import random
import collections
import math
import matplotlib.pyplot as plt
train_file=""
test_file=""

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
for i in range(len(test)):
	scores[test[i][0]]=model.infer_vector(gensim.utils.simple_preprocess(test[i][1]))
#computing similarity
def cos_similarity(vector_one,vector_two):
	s=0.
	for i in range(len(vector_one)):
		s+=vector_one[i]*vector_two[i]
	One=0.
	Two=0.
	for i in range(len(vector_one)):
		One+=vector_one[i]*vector_one[i]
	One=math.sqrt(One)
	for i in range(len(vector_two)):
		Two+=vector_two[i]*vector_two[i]
	Two=math.sqrt(Two)
	return s/(One*Two)

#ranking similarity
keys=scores.keys()
result={}
x=[]
y=[]
for i in range(len(keys)):
	val=-1
	index=i
	x.append(i)
	for j in range(len(keys)):
		if i==j:
			continue
		else:
			cos=cos_similarity(scores[keys[i]],scores[keys[j]])
			if cos>val:
				val=cos
				index=j
	y.append(val)
	result[keys[i]]=keys[index]
plt.plot(x,y)
plt.show()
if not os.path.isfile('result.txt'):
	f=open("result.txt",'w')
	for key in result.keys():
		f.write(key+' '+result[key]+'\n')
	f.close()