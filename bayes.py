"""
use naive bayes to build classifier and process 209321 tweets in my MongoDB database
"""
import pymongo
import nltk
import io
try:
    import json
except ImportError:
    import simplejson as json
from collections import Counter
from prettytable import PrettyTable
from sklearn.naive_bayes import MultinomialNB
from nltk.corpus import stopwords
from sklearn import cross_validation

def setOfWords2Vec(vocabList, inputSet) :
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
    return returnVec

def get_diversity(tokens):
    return 1.0 * len(set(tokens)) / len(tokens)

def average_words(statuses):
    total_words = sum([len(s.split()) for s in statuses])
    return 1.0*total_words/len(statuses)

connection = pymongo.MongoClient()
db = connection['test-data8']
coll = db['total3']
num = coll.count()
print 'number of tweets', num

total_text = [i for i in coll.distinct('text')]


y = [0]*len(total_text)
print 'number of unique tweets', len(y)

words_total = [w
         for t in total_text
             for w in t.split()]

kind = set(words_total)
print 'kinds of words', len(set(words_total))
print 'lexical_diversity: ', get_diversity(words_total)
print 'average_words: ', len(words_total) * 1.0 / coll.count()


english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
english_stopwords = stopwords.words('english')


for i in range(len(total_text)):
    if ':)' in total_text[i]:
        y[i] = 1
    else:
        y[i] = 0

X_train, X_test, y_train, y_test = cross_validation.train_test_split(total_text,y,test_size=0.3,random_state=20160318)

print 'size of train set:', len(X_train)
print 'size of test set:', len(X_test)


words = [[w
         for w in document.split()] for document in X_train]


texts_filtered_stopwords = [[word for word in document if not word in english_stopwords] for document in words]
texts_filtered = [[word for word in document if not word in english_punctuations] for document in words]

all_words = []
for document in texts_filtered:
    for word in document:
        if len(word) > 2:
            all_words.append(word.lower())

all_words2 = nltk.FreqDist(w.lower() for w in all_words)
#all_words2.plot(100,cumulative=False)
wordlist = [fpair[0] for fpair in list(all_words2.most_common(13000))]

print 'length of Wordlist', len(wordlist)


X_test2 = []
for i in X_test:
    X_test2.append(i.lower())

X_test = X_test2


nbClf = MultinomialNB(alpha=1)

train_data = [([0] * len(wordlist)) for i in range(len(y_train))]

for i in range(len(train_data)):
    words = [w
         for w in X_train[i].split()]
    train_data[i] = setOfWords2Vec(wordlist, words)

test_data = [([0] * len(wordlist)) for i in range(len(y_test))]

for i in range(len(test_data)):
    words = [w
         for w in X_test[i].split()]
    test_data[i] = setOfWords2Vec(wordlist, words)



nbClf.fit(train_data, y_train)

print 'finish training!'
print 'accuracy:', nbClf.score(test_data, y_test)