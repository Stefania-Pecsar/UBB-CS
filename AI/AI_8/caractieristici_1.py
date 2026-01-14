import csv
import os
from sklearn.feature_extraction.text import CountVectorizer

#load some data
crtDir = os.getcwd()
fileName = os.path.join(crtDir,'data','reviews_mixed.csv')

data = []
with open(fileName, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            dataNames = row
        else:
            data.append(row)
        line_count += 1

inputs = [data[i][0] for i in range(len(data))][:225]
outputs = [data[i][1] for i in range(len(data))][:225]
labelNames = list(set(outputs))

print(inputs[:225])
print()
print(labelNames[:225])
print()

# prepare data for training and testing

import numpy as np

np.random.seed(5)
# noSamples = inputs.shape[0]
noSamples = len(inputs)
indexes = [i for i in range(noSamples)]
trainSample = np.random.choice(indexes, int(0.8 * noSamples), replace = False)
testSample = [i for i in indexes  if not i in trainSample]

trainInputs = [inputs[i] for i in trainSample]
trainOutputs = [outputs[i] for i in trainSample]
testInputs = [inputs[i] for i in testSample]
testOutputs = [outputs[i] for i in testSample]

print(trainInputs[:3])
print()

# extract some features from the raw text

# # representation Bag of Words
vectorizer = CountVectorizer()

trainFeatures = vectorizer.fit_transform(trainInputs)
testFeatures = vectorizer.transform(testInputs)

# vocabulary size
print("vocab size: ", len(vectorizer.vocabulary_),  " words")
print()
# no of reviews (Samples)
print("traindata size: ", len(trainInputs), " reviews")
print()
# shape of feature matrix
print("trainFeatures shape: ", trainFeatures.shape)
print()
# vocabbulary from the train data 
print('some words of the vocab: ', vectorizer.get_feature_names_out()[-20:])
print()
# extracted features
print('some features: ', trainFeatures.toarray()[:3])
print()