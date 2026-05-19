import os
import csv
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import numpy as np 
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from math import sqrt

# doar de Produsul intern brut

#SGD = socastic 
#GD-batch

def loadData(fileName, inputVariabName, outputVariabName):
    data = []
    dataNames = []
    with open(fileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                dataNames = row
            else:
                data.append(row)
            line_count += 1
    selectedVariable = dataNames.index(inputVariabName)
    inputs = [float(data[i][selectedVariable]) for i in range(len(data))]
    selectedOutput = dataNames.index(outputVariabName)
    outputs = [float(data[i][selectedOutput]) for i in range(len(data))]
    
    return inputs, outputs

crtDir =  os.getcwd()
filePath = os.path.join(crtDir, 'D:/fac/AN 2/AI/AI_6/GradFericire', 'world-happiness-report-2017.csv')

inputs, outputs = loadData(filePath, 'Economy..GDP.per.Capita.', 'Happiness.Score')
print('in:  ', inputs[:5])
print('out: ', outputs[:5])

# def plotDataHistogram(x, variableName):
#     n, bins, patches = plt.hist(x, 10)
#     plt.title('Histogram of ' + variableName)
#     plt.show()

# plotDataHistogram(inputs, "capita GDP")
# plotDataHistogram(outputs, "Happiness score")

# plt.plot(inputs, outputs, 'ro') 
# plt.xlabel('GDP capita')
# plt.ylabel('happiness')
# plt.title('GDP capita vs. happiness')
# plt.show()

np.random.seed(5)
indexes = [i for i in range(len(inputs))]
trainSample = np.random.choice(indexes, int(0.8 * len(inputs)), replace = False)
testSample = [i for i in indexes  if not i in trainSample]

trainInputs = [inputs[i] for i in trainSample]
trainOutputs = [outputs[i] for i in trainSample]

testInputs = [inputs[i] for i in testSample]
testOutputs = [outputs[i] for i in testSample]

# plt.plot(trainInputs, trainOutputs, 'ro', label = 'training data')   #train data 
# plt.plot(testInputs, testOutputs, 'g^', label = 'testing data')     #test data 
# plt.title('train and test data')
# plt.xlabel('GDP capita')
# plt.ylabel('happiness')
# plt.legend()
# plt.show()

xx = [[el] for el in trainInputs]

# Inițializăm regresorul pentru gradientul descendent cu batch-uri
regressor = linear_model.SGDRegressor(alpha=0.0000001, max_iter=1000)

# Definim dimensiunea lotului
batch_size = 100

# Antrenăm modelul folosind gradientul descendent cu batch-uri
for i in range(0, len(trainInputs), 1):
    X_batch = [[el] for el in trainInputs[i:i+batch_size]]  # Transformăm într-o listă de liste
    y_batch = trainOutputs[i:i+batch_size]
    regressor.partial_fit(X_batch, y_batch)

# Obținem parametrii modelului
w0, w1 = regressor.intercept_[0], regressor.coef_[0]


# Afișăm modelul învățat
#print("SGD:   f(x) = 2.750859810931838  +  2.5537184851664714  * x")
print('GD - batch: f(x) = ', w0, ' + ', w1, ' * x' )

noOfPoints = 1000
xref = []
val = min(trainInputs)
step = (max(trainInputs) - min(trainInputs)) / noOfPoints
for i in range(1, noOfPoints):
    xref.append(val)
    val += step
yref = [w0 + w1 * el for el in xref] 

plt.plot(trainInputs, trainOutputs, 'ro', label = 'training data')  #train data are plotted by red and circle sign
plt.plot(xref, yref, 'b-', label = 'learnt model')                  #model is plotted by a blue line
plt.title('train data and the learnt model')
plt.xlabel('GDP capita')
plt.ylabel('happiness')
plt.legend()
plt.show()

computedTestOutputs = regressor.predict([[x] for x in testInputs])

# plot the computed outputs (see how far they are from the real outputs)
plt.plot(testInputs, computedTestOutputs, 'yo', label = 'computed test data')  #computed test data are plotted yellow red and circle sign
plt.plot(testInputs, testOutputs, 'g^', label = 'real test data')  #real test data are plotted by green triangles
plt.title('computed test and real test data')
plt.xlabel('GDP capita')
plt.ylabel('happiness')
plt.legend()
plt.show()

error = 0.0
for t1, t2 in zip(computedTestOutputs, testOutputs):
    error += (t1 - t2) ** 2
error = error / len(testOutputs)

error = mean_squared_error(testOutputs, computedTestOutputs)

print("SGD")
print("prediction error (manual):  0.44566059276524816")
print("prediction error (tool):   0.4456605927652483")
print("GD")
print('prediction error (manual): ', error)
print('prediction error (tool):  ', error)

def loadDataMoreInputs(fileName, inputVariabNames, outputVariabName):
    data = []
    dataNames = []
    with open(fileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                dataNames = row
            else:
                data.append(row)
            line_count += 1
    selectedVariable1 = dataNames.index(inputVariabNames[0])
    selectedVariable2 = dataNames.index(inputVariabNames[1])
    inputs = [[float(data[i][selectedVariable1]), float(data[i][selectedVariable2])] for i in range(len(data))]
    selectedOutput = dataNames.index(outputVariabName)
    outputs = [float(data[i][selectedOutput]) for i in range(len(data))]
    
    return inputs, outputs

def plot3Ddata(x1Train, x2Train, yTrain, x1Model=None, x2Model=None, yModel=None, x1Test=None, x2Test=None, yTest=None, title=None):
    
    ax = plt.axes(projection='3d')
    
    if x1Train is not None:
        ax.scatter(x1Train, x2Train, yTrain, c='r', marker='o', label='train data')
    if x1Model is not None:
        ax.scatter(x1Model, x2Model, yModel, c='b', marker='_', label='learnt model')
    if x1Test is not None:
        ax.scatter(x1Test, x2Test, yTest, c='g', marker='^', label='test data')
    
    plt.title(title)
    ax.set_xlabel("capita")
    ax.set_ylabel("freedom")
    ax.set_zlabel("happiness")
    plt.legend()
    plt.show()

crtDir =  os.getcwd()
filePath = os.path.join(crtDir, 'D:/fac/AN 2/AI/AI_6/GradFericire', 'world-happiness-report-2017.csv')

inputs, outputs = loadDataMoreInputs(filePath, ['Economy..GDP.per.Capita.', 'Freedom'], 'Happiness.Score')

inputs, outputs = loadDataMoreInputs(filePath, ['Economy..GDP.per.Capita.', 'Freedom'], 'Happiness.Score')

feature1 = [ex[0] for ex in inputs]
feature2 = [ex[1] for ex in inputs]

# plot the data histograms
# plotDataHistogram(feature1, 'capita GDP')
# plotDataHistogram(feature2, 'freedom')
# plotDataHistogram(outputs, 'Happiness score')

# check the liniarity (to check that a linear relationship exists between the dependent variable (y = happiness) and the independent variables (x1 = capita, x2 = freedom).)
#plot3Ddata(feature1, feature2, outputs, [], [], [], [], [], [], 'capita vs freedom vs happiness')

def normalisation(trainData, testData):
    scaler = StandardScaler()
    if not isinstance(trainData[0], list):
        #encode each sample into a list
        trainData = [[d] for d in trainData]
        testData = [[d] for d in testData]
        
        scaler.fit(trainData)  #  fit only on training data
        normalisedTrainData = scaler.transform(trainData) # apply same transformation to train data
        normalisedTestData = scaler.transform(testData)  # apply same transformation to test data
        
        #decode from list to raw values
        normalisedTrainData = [el[0] for el in normalisedTrainData]
        normalisedTestData = [el[0] for el in normalisedTestData]
    else:
        scaler.fit(trainData)  #  fit only on training data
        normalisedTrainData = scaler.transform(trainData) # apply same transformation to train data
        normalisedTestData = scaler.transform(testData)  # apply same transformation to test data
    return normalisedTrainData, normalisedTestData

np.random.seed(5)
indexes = [i for i in range(len(inputs))]
trainSample = np.random.choice(indexes, int(0.8 * len(inputs)), replace = False)
testSample = [i for i in indexes  if not i in trainSample]

trainInputs = [inputs[i] for i in trainSample]
trainOutputs = [outputs[i] for i in trainSample]
testInputs = [inputs[i] for i in testSample]
testOutputs = [outputs[i] for i in testSample]


trainInputs, testInputs = normalisation(trainInputs, testInputs)
trainOutputs, testOutputs = normalisation(trainOutputs, testOutputs)

feature1train = [ex[0] for ex in trainInputs]
feature2train = [ex[1] for ex in trainInputs]

feature1test = [ex[0] for ex in testInputs]
feature2test = [ex[1] for ex in testInputs]

#plot3Ddata(feature1train, feature2train, trainOutputs, None, None, None, feature1test, feature2test, testOutputs, "train and test data (after normalisation)")

# Inițializăm regresorul
regressor = linear_model.SGDRegressor(alpha=0.00001, max_iter=1000)

# Definim dimensiunea lotului
batch_size = 110

# Antrenăm modelul folosind gradientul descendent cu batch-uri
for i in range(0, len(trainInputs), 5):
    X_batch = trainInputs[i:i+batch_size]
    y_batch = trainOutputs[i:i+batch_size]
    regressor.partial_fit(X_batch, y_batch)

# Obținem parametrii modelului
w0, w1, w2 = regressor.intercept_, regressor.coef_[0], regressor.coef_[1]

# Afișăm modelul învățat
print("SGD: f(x) =  [-0.00185396]  +  0.671689108706825  * x1 +  0.3188107120116774  * x2")
print('GD - batch: f(x) = ', w0, ' + ', w1, ' * x1 + ', w2, ' * x2' )

noOfPoints = 20
xref1 = []
val = min(feature1)
step1 = (max(feature1) - min(feature1)) / noOfPoints
for _ in range(1, noOfPoints):
    for _ in range(1, noOfPoints):
        xref1.append(val)
    val += step1

xref2 = []
val = min(feature2)
step2 = (max(feature2) - min(feature2)) / noOfPoints
for _ in range(1, noOfPoints):
    aux = val
    for _ in range(1, noOfPoints):
        xref2.append(aux)
        aux += step2
yref = [w0 + w1 * el1 + w2 * el2 for el1, el2 in zip(xref1, xref2)]
plot3Ddata(feature1train, feature2train, trainOutputs, xref1, xref2, yref, [], [], [], 'train data and the learnt model')

computedTestOutputs = regressor.predict(testInputs)

# plot3Ddata([], [], [], feature1test, feature2test, computedTestOutputs, feature1test, feature2test, testOutputs, 'predictions vs real test data')


error = 0.0
for t1, t2 in zip(computedTestOutputs, testOutputs):
    error += (t1 - t2) ** 2
error = error / len(testOutputs)

errorMAE = 0.0
errorMAE = sum(abs(computedTestOutputs[i] - testOutputs[i]) for i in range(len(testOutputs))) / len(testOutputs)

errorRMSE = 0.0
errorRMSE = np.mean((np.array(computedTestOutputs) - np.array(testOutputs)) ** 2)
errorRMSE = np.sqrt(errorRMSE)

error1 = mean_squared_error(testOutputs, computedTestOutputs)

print("SGD")
print("prediction error (manual):  0.22784041508275105")
print("prediction error (tool):    0.22784041508275105")
print("GD-batch")
print('prediction error (manual- MSE): ', error)
print('prediction error (manual- MAE): ', errorMAE)
print('prediction error (manual- RMSE): ', errorRMSE)
print('prediction error (tool):   ', error1)