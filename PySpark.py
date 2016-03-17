"""
Notice that this program is for PySpark which handle 1 million tweets.
1.Read train set and data set from txt files.
2.Put data set into Spark system, and transform them into RDD.
3.Run the bayse algorithm from MLlib. 
"""
from pyspark.mllib.classification import NaiveBayes
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint

def parseLine(line):
    parts = line.split(', #')
    label = float(parts[0])
    features = Vectors.dense([float(x) for x in parts[1].split('#')])
    return LabeledPoint(label, features)

tr1 = sc.textFile('/Users/yuanjun/Desktop/train1.txt').map(parseLine)
tr2 = sc.textFile('/Users/yuanjun/Desktop/train2.txt').map(parseLine)
tr3 = sc.textFile('/Users/yuanjun/Desktop/train3.txt').map(parseLine)
tr4 = sc.textFile('/Users/yuanjun/Desktop/train4.txt').map(parseLine)
te1 = sc.textFile('/Users/yuanjun/Desktop/test1.txt').map(parseLine)
te2 = sc.textFile('/Users/yuanjun/Desktop/test2.txt').map(parseLine)

tr1 = tr1.union(tr2)
tr3 = tr3.union(tr4)
train = tr1.union(tr3)
test = te1.union(te2)

model = NaiveBayes.train(train, 1.0)
predictionAndLabel = test.map(lambda p : (model.predict(p.features), p.label))
accuracy = 1.0 * predictionAndLabel.filter(lambda (x, v): x == v).count() / test.count()
print accuracy
