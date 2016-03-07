"""
This program process all 1247391 tweets I collcted in my database. 
Transform each tweet into a vector by comparing words in wordlist.
Save 70% tweets as train set 30% tweets as test set into txt files.

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
            returnVec[vocabList.index(word)]= 1
    return returnVec

def get_diversity(tokens):
    return 1.0 * len(set(tokens)) / len(tokens)

def average_words(statuses):
    total_words = sum([len(s.split()) for s in statuses])
    return 1.0*total_words/len(statuses)


total_text = []
connection = pymongo.MongoClient()
db = connection['test-data8']
collection = ['negtive_data', 'negtive_data2', 'negtive_data3', 'positive_data', 'positive_data2', 'positive_data3']

for i in collection:
    coll = db[i]
    num = coll.count()
    print 'number of tweets', num
    text = [i for i in coll.distinct('text')]
    for j in text:
        total_text.append(j)


y = [0]*len(total_text)
print 'number of unique tweets', len(y)

words_total = [w
         for t in total_text
             for w in t.split()]


english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
english_stopwords = stopwords.words('english')


for i in range(len(total_text)):
    if ':)' in total_text[i]:
        y[i] = 1.0
    else:
        y[i] = 0.0

X_train, X_test, y_train, y_test = cross_validation.train_test_split(total_text,y,test_size=0.3,random_state=0)

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
wordlist = [fpair[0] for fpair in list(all_words2.most_common(13000))]

print 'length of Wordlist', len(wordlist)


X_a= []
for i in X_test:
    X_a.append(i.lower())

X_test = X_a

X_traina, X_trainb, y_traina, y_trainb = cross_validation.train_test_split(X_train,y_train,test_size=0.5,random_state=0)
X_train1, X_train2, y_train1, y_train2 = cross_validation.train_test_split(X_traina,y_traina,test_size=0.5,random_state=0)
X_train3, X_train4, y_train3, y_train4 = cross_validation.train_test_split(X_trainb,y_trainb,test_size=0.5,random_state=0)
X_test1, X_test2, y_test1, y_test2 = cross_validation.train_test_split(X_test,y_test,test_size=0.5,random_state=0)

print 'size of train1 set:', len(X_train1)
print 'size of train2 set:', len(X_train2)
print 'size of train3 set:', len(X_train3)
print 'size of train4 set:', len(X_train4)
print 'size of test1 set:', len(X_test1)
print 'size of test2 set:', len(X_test2)

ftr1 = open('/Users/yuanjun/Desktop/train1.txt', 'w')
print "open ftr1"
train_data1 = [([0] * len(wordlist)) for i in range(len(y_train1))]

for i in range(len(train_data1)):
    words = [w
         for w in X_train1[i].split()]
    train_data1[i] = setOfWords2Vec(wordlist, words)
    s = ""
    for j in train_data1[i]:
        s = s + "#" + str(j)
    print >>ftr1, str(y_train1[i])+",",s
ftr1.close()
print "write train1 done!"


ftr2 = open('/Users/yuanjun/Desktop/train2.txt', 'w')
print "open ftr2"
train_data2 = [([0] * len(wordlist)) for i in range(len(y_train2))]

for i in range(len(train_data2)):
    words = [w
         for w in X_train2[i].split()]
    train_data2[i] = setOfWords2Vec(wordlist, words)
    s = ""
    for j in train_data2[i]:
        s = s + "#" + str(j)
    print >>ftr2, str(y_train2[i])+",",s
ftr2.close()
print "write train2 done!"


ftr3 = open('/Users/yuanjun/Desktop/train3.txt', 'w')
print "open ftr3"
train_data3 = [([0] * len(wordlist)) for i in range(len(y_train3))]

for i in range(len(train_data3)):
    words = [w
         for w in X_train3[i].split()]
    train_data3[i] = setOfWords2Vec(wordlist, words)
    s = ""
    for j in train_data3[i]:
        s = s + "#" + str(j)
    print >>ftr3, str(y_train3[i])+",",s
ftr3.close()
print "write train3 done!"


ftr4 = open('/Users/yuanjun/Desktop/train4.txt', 'w')
print "open ftr4"
train_data4 = [([0] * len(wordlist)) for i in range(len(y_train4))]

for i in range(len(train_data4)):
    words = [w
         for w in X_train4[i].split()]
    train_data4[i] = setOfWords2Vec(wordlist, words)
    s = ""
    for j in train_data4[i]:
        s = s + "#" + str(j)
    print >>ftr4, str(y_train4[i])+",",s
ftr4.close()
print "write train4 done!"


fte1 = open('/Users/yuanjun/Desktop/test1.txt', 'w')
print "open fte1"
test_data1 = [([0] * len(wordlist)) for i in range(len(y_test1))]

for i in range(len(test_data1)):
    words = [w
         for w in X_test1[i].split()]
    test_data1[i] = setOfWords2Vec(wordlist, words)
    s = ""
    for j in test_data1[i]:
        s = s + "#" + str(j)
    print >>fte1, str(y_test1[i])+",",s

fte1.close()
print "write test1 done!"

fte2 = open('/Users/yuanjun/Desktop/test2.txt', 'w')
print "open fte2"
test_data2 = [([0] * len(wordlist)) for i in range(len(y_test2))]

for i in range(len(test_data2)):
    words = [w
         for w in X_test2[i].split()]
    test_data2[i] = setOfWords2Vec(wordlist, words)
    s = ""
    for j in test_data2[i]:
        s = s + "#" + str(j)
    print >>fte2, str(y_test2[i])+",",s

fte2.close()
print "write test2 done!"