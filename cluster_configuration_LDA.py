import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
from gensim import corpora, models
from pprint import pprint
np.random.seed(2018)
import nltk
nltk.download('wordnet')

list_of_file=["apache-configuration","hdfs-configuration","mysql-configuration","php-configuration"]

def lemmatize_stemming(text):
	stemmer = PorterStemmer()
	return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))
def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            #result.append(lemmatize_stemming(token))
            result.append(token)
    return result
def read_file():
	result=[]
	for f in list_of_file:
		lines=open(f,'r')
		for line in lines:
			result.append(line.split('**')[1])
	return result

raw_content=read_file()
processed_docs=[]
for c in raw_content:
	processed_docs.append(preprocess(c))
dictionary = gensim.corpora.Dictionary(processed_docs)
dictionary.filter_extremes(no_below=5, no_above=0.5, keep_n=100000)
bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]
tfidf = models.TfidfModel(bow_corpus)
corpus_tfidf = tfidf[bow_corpus]
lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics=4, id2word=dictionary, passes=2, workers=2)
for idx, topic in lda_model.print_topics(-1):print('Topic: {} \nWords: {}'.format(idx, topic))

#for index, score in sorted(lda_model[bow_corpus[4310]], key=lambda tup: -1*tup[1]):
#    print("\nScore: {}\t \nTopic: {}".format(score, lda_model.print_topic(index, 10)))
