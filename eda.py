"""
realize eda process to tweets and compare the results with Gutenberg text, such as average words and lexical diversity

"""
import pymongo
import nltk
from nltk.book import *
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
            #print "the word:%s is in my Vocabulary!" % word
    return returnVec

def get_diversity(tokens):
    return 1.0 * len(set(tokens)) / len(tokens)

def average_words(statuses):
    total_words = sum([len(s.split()) for s in statuses])
    return 1.0*total_words/len(statuses)

connection = pymongo.MongoClient()
db = connection['test-data8']
neg = ['negtive_data', 'negtive_data2', 'negtive_data3']
pos = ['positive_data', 'positive_data2', 'positive_data3']
total_neg = []
total_pos = []
total_text = []
num1 = 0
num2 = 0

for i in neg:
    coll = db[i]
    num = coll.count()
    num1 = num1 + num
    #print 'number of negative tweets', num
    text = [i for i in coll.distinct('text')]
    for j in text:
        total_neg.append(j)
        total_text.append(j)

for i in pos:
    coll = db[i]
    num = coll.count()
    num2 = num2 + num
    #print 'number of positive tweets', num
    text = [i for i in coll.distinct('text')]
    for j in text:
        total_pos.append(j)
        total_text.append(j)


diversity = 0
average_words = 0
source = nltk.corpus.gutenberg.fileids()
for i in source:
    text_words = gutenberg.words(i)
    diversity = diversity + get_diversity(text_words)
    num_words = len(gutenberg.words(i))
    num_sents = len(gutenberg.sents(i))
    average_words = average_words + round(num_words/num_sents)

print "text words diversity: ", diversity*1.0/18
print "text average word in sentence: ", average_words/18

y = [0]*len(total_text)
print 'number of positive tweets', num2
print 'number of negative tweets', num1
print 'number of tweets', len(y)


words_total = [w
         for t in total_text
             for w in t.split()]

words_neg = [w
         for t in total_neg
             for w in t.split()]

words_pos = [w
         for t in total_pos
             for w in t.split()]


kind = set(words_total)
print 'total kinds of words', len(set(words_total))
print 'tweet_lexical_diversity: ', get_diversity(words_total)
print 'tweet_average_words: ', len(words_total) * 1.0 / len(y)

kind = set(words_neg)
print 'kinds of neg words', len(set(words_neg))
print 'neg tweet_lexical_diversity: ', get_diversity(words_neg)
print 'neg tweet_average_words: ', len(words_neg) * 1.0 / num1

kind = set(words_pos)
print 'total kinds of words', len(set(words_pos))
print 'pos tweet_lexical_diversity: ', get_diversity(words_pos)
print 'pos tweet_average_words: ', len(words_pos) * 1.0 / num2

english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
english_stopwords = stopwords.words('english')

for i in range(len(total_text)):
    if ':)' in total_text[i]:
        y[i] = 1
    else:
        y[i] = 0

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
all_words2.plot(100, cumulative=False)
wordlist = [fpair[0] for fpair in list(all_words2.most_common(13000))]
print 'length of Wordlist', len(wordlist)
