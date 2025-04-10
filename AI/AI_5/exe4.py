import csv
import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from math import log,sqrt

def standardNormalize(data):
    mean = np.mean(data)
    std_dev = np.std(data)
    normalized_data = (data - mean) / std_dev
    return normalized_data

# doar de Produsul intern brut (exemplu detaliat live - demo)

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
    inputs = [float(row[selectedVariable]) if row[selectedVariable] != '' else None for row in data]
    selectedOutput = dataNames.index(outputVariabName)
    outputs = [float(row[selectedOutput]) for row in data]

    # calculam media la valorile input
    values = [float(row[selectedVariable]) for row in data if row[selectedVariable] != '' and row[selectedVariable] != 0]
    mean_value = sum(values) / len(values)
    
    # Înlocuim valorile nule cu media calculată
    for i in range(len(inputs)):
        if inputs[i] is None or inputs[i]==0:
            inputs[i] = mean_value

    inputs = standardNormalize(inputs)
    outputs = standardNormalize(outputs)
    
    return inputs, outputs
    
crtDir =  os.getcwd()
filePath = os.path.join(crtDir, 'data', 'D:/lab5/v3_world-happiness-report-2017.csv')

inputs, outputs = loadData(filePath, 'Economy..GDP.per.Capita.', 'Happiness.Score')
print('in:  ', inputs[:5])
print('out: ', outputs[:5])


def plotDataHistogram(x, variableName):
    n, bins, patches = plt.hist(x, 10)
    plt.title('Histogram of ' + variableName)
    plt.show()

plotDataHistogram(inputs, 'capita GDP')
plotDataHistogram(outputs, 'Happiness score')


plt.plot(inputs, outputs, 'ro') 
plt.xlabel('GDP capita')
plt.ylabel('happiness')
plt.title('GDP capita vs. happiness')
plt.show()

np.random.seed(5)
indexes = [i for i in range(len(inputs))]

trainSample = np.random.choice(indexes, int(0.8 * len(inputs)), replace = False)
validationSample = [i for i in indexes  if not i in trainSample]

trainInputs = [inputs[i] for i in trainSample]
trainOutputs = [outputs[i] for i in trainSample]

validationInputs = [inputs[i] for i in validationSample]
validationOutputs = [outputs[i] for i in validationSample]

plt.plot(trainInputs, trainOutputs, 'ro', label = 'training data')   #train data 
plt.plot(validationInputs, validationOutputs, 'g^', label = 'validation data')     #test data 
plt.title('train and validation data')
plt.xlabel('GDP capita')
plt.ylabel('happiness')
plt.legend()
plt.show()

xx = [[el] for el in trainInputs]


regressor = linear_model.LinearRegression()
regressor.fit(xx, trainOutputs)
w0, w1 = regressor.intercept_, regressor.coef_[0]
print('the learnt model: f(x) = ', w0, ' + ', w1, ' * x')


# plot the learnt model
noOfPoints = 1000
xref = []
val = min(trainInputs)
step = (max(trainInputs) - min(trainInputs)) / noOfPoints
for i in range(1, noOfPoints):
    xref.append(val)
    val += step
yref = [w0 + w1 * el for el in xref] 

plt.plot(trainInputs, trainOutputs, 'ro', label = 'training data')  #train data 
plt.plot(xref, yref, 'b-', label = 'learnt model')                  #model 
plt.title('train data and the learnt model')
plt.xlabel('GDP capita')
plt.ylabel('happiness')
plt.legend()
plt.show()


computedValidationOutputs = regressor.predict([[x] for x in validationInputs])


plt.plot(validationInputs, computedValidationOutputs, 'yo', label = 'computed test data')  #computed test data 
plt.plot(validationInputs, validationOutputs, 'g^', label = 'real test data')  #real test data 
plt.title('computed validation and real validation data')
plt.xlabel('GDP capita')
plt.ylabel('happiness')
plt.legend()
plt.show()


error = 0.0
for t1, t2 in zip(computedValidationOutputs, validationOutputs):
    error += (t1 - t2) ** 2
error = error / len(validationOutputs)
print("Normalizare")
print('prediction error (manual): ', error)

# by using sklearn 
from sklearn.metrics import mean_squared_error

error = mean_squared_error(validationOutputs, computedValidationOutputs)
print('prediction error (tool):  ', error)

print("Fara normalizare:")
print("prediction error (manual):  0.4198256047384838")
print("prediction error (tool):   0.4198256047384838")


# doar de caracteristica "Family" (tema):

def loadData(fileName,inputVariabNume,outputVariabNume):
    data=[]
    dataNames=[]
    with open(fileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                dataNames = row
            else:
                data.append(row)
            line_count += 1

    selectedVariable = dataNames.index(inputVariabNume)
    inputs = [float(row[selectedVariable]) if row[selectedVariable] != '' else None for row in data]
    selectedOutput = dataNames.index(outputVariabNume)
    outputs = [float(row[selectedOutput]) for row in data]

    # calculam media la valorile input
    values = [float(row[selectedVariable]) for row in data if row[selectedVariable] != '' and row[selectedVariable] != 0]
    mean_value = sum(values) / len(values)

    # Înlocuim valorile nule cu media calculată
    for i in range(len(inputs)):
        if inputs[i] is None or inputs[i]==0:
            inputs[i] = mean_value

    inputs = standardNormalize(inputs)
    outputs = standardNormalize(outputs)
    
    return inputs, outputs
    
crtDir =  os.getcwd()
filePath = os.path.join(crtDir, 'data', 'D:/lab5/v3_world-happiness-report-2017.csv')

inputs, outputs = loadData(filePath, 'Family', 'Happiness.Score')
print('in:  ', inputs[:5])
print('out: ', outputs[:5])

def plotDataHistogram(x, variableName):
    n, bins, patches = plt.hist(x, 10)
    plt.title('Histogram of ' + variableName)
    plt.show()

plotDataHistogram(inputs, 'Family')
plotDataHistogram(outputs, 'Happiness score')


plt.plot(inputs, outputs, 'ro') 
plt.xlabel('Family')
plt.ylabel('happiness')
plt.title('Family vs. happiness')
plt.show()

np.random.seed(5)
indexes = [i for i in range(len(inputs))]

trainSample = np.random.choice(indexes, int(0.8 * len(inputs)), replace = False)
validationSample = [i for i in indexes  if not i in trainSample]

trainInputs = [inputs[i] for i in trainSample]
trainOutputs = [outputs[i] for i in trainSample]

validationInputs = [inputs[i] for i in validationSample]
validationOutputs = [outputs[i] for i in validationSample]

plt.plot(trainInputs, trainOutputs, 'ro', label = 'training data')   #train data 
plt.plot(validationInputs, validationOutputs, 'g^', label = 'validation data')     #test data 
plt.title('train and validation data')
plt.xlabel('Family')
plt.ylabel('happiness')
plt.legend()
plt.show()

xx = [[el] for el in trainInputs]


regressor = linear_model.LinearRegression()
regressor.fit(xx, trainOutputs)
w0, w1 = regressor.intercept_, regressor.coef_[0]
print('the learnt model: f(x) = ', w0, ' + ', w1, ' * x')


# plot the learnt model
noOfPoints = 1000
xref = []
val = min(trainInputs)
step = (max(trainInputs) - min(trainInputs)) / noOfPoints
for i in range(1, noOfPoints):
    xref.append(val)
    val += step
yref = [w0 + w1 * el for el in xref] 

plt.plot(trainInputs, trainOutputs, 'ro', label = 'training data')  #train data 
plt.plot(xref, yref, 'b-', label = 'learnt model')                  #model 
plt.title('train data and the learnt model')
plt.xlabel('Family')
plt.ylabel('happiness')
plt.legend()
plt.show()


computedValidationOutputs = regressor.predict([[x] for x in validationInputs])


plt.plot(validationInputs, computedValidationOutputs, 'yo', label = 'computed test data')  #computed test data 
plt.plot(validationInputs, validationOutputs, 'g^', label = 'real test data')  #real test data 
plt.title('computed validation and real validation data')
plt.xlabel('Family')
plt.ylabel('happiness')
plt.legend()
plt.show()


error = 0.0
for t1, t2 in zip(computedValidationOutputs, validationOutputs):
    error += (t1 - t2) ** 2
error = error / len(validationOutputs)
print("Normalizare:")
print('prediction error (manual): ', error)

error = mean_squared_error(validationOutputs, computedValidationOutputs)
print('prediction error (tool):  ', error)

print("Fara normalizare:")
print("prediction error (manual):  0.5897568470925796")
print("prediction error (tool):   0.5897568470925795")


# de Produsul intern brut si de gradul de libertate (temă).

def loadData(fileName, inputVariabName1, inputVariabName2, outputVariabName):
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
    selectedVariable1 = dataNames.index(inputVariabName1)
    inputs1 = [float(row[selectedVariable1]) if row[selectedVariable1] != '' else None for row in data]
    selectedVariable2 = dataNames.index(inputVariabName2)
    inputs2 = [float(row[selectedVariable2]) if row[selectedVariable2] != '' else None for row in data]

    mean_value1 = sum([val for val in inputs1 if val is not None]) / len([val for val in inputs1 if val is not None])
    mean_value2 = sum([val for val in inputs2 if val is not None]) / len([val for val in inputs2 if val is not None])

    for i in range(len(inputs1)):
        if inputs1[i] is None:
            inputs1[i] = mean_value1
        if inputs2[i] is None:
            inputs2[i] = mean_value2

    selectedOutput = dataNames.index(outputVariabName)
    outputs = [float(row[selectedOutput]) for row in data]


    inputs1 = standardNormalize(inputs1)
    inputs2 = standardNormalize(inputs2)
    outputs = standardNormalize(outputs)
    
    return inputs1, inputs2, outputs


crtDir = os.getcwd()
filePath = os.path.join(crtDir, 'data', 'D:/lab5/v3_world-happiness-report-2017.csv')

inputs1, inputs2, outputs = loadData(filePath, 'Economy..GDP.per.Capita.', 'Freedom', 'Happiness.Score')
print('in1: ', inputs1[:5])
print('in2: ', inputs2[:5])
print('out: ', outputs[:5])

# Plot the histograms associated with input data and output data

def plotDataHistogram(x, variableName):
    n, bins, patches = plt.hist(x, 10)
    plt.title('Histogram of ' + variableName)
    plt.show()

plotDataHistogram(inputs1, 'Economy..GDP.per.Capita.')
plotDataHistogram(inputs2, 'Freedom')
plotDataHistogram(outputs, 'Happiness score')

# Check linearity

plt.plot(inputs1, outputs, 'ro', label='Economy..GDP.per.Capita.') 
plt.plot(inputs2, outputs, 'g^', label='Freedom') 
plt.xlabel('Input Variables')
plt.ylabel('Happiness Score')
plt.title('Economy..GDP.per.Capita. and Freedom vs. Happiness')
plt.legend()
plt.show()

# Combine inputs into one matrix
X = np.column_stack((inputs1, inputs2))


np.random.seed(5)
indexes = np.arange(len(inputs1))

trainSample = np.random.choice(indexes, int(0.8 * len(inputs1)), replace=False)
validationSample = np.array([i for i in indexes if i not in trainSample])

trainInputs = X[trainSample]
trainOutputs = np.array([outputs[i] for i in trainSample])

validationInputs = X[validationSample]
validationOutputs = np.array([outputs[i] for i in validationSample])

# Plot train and validation data
plt.plot(trainInputs[:,0], trainOutputs, 'ro', label='Training data (GDP)')   
plt.plot(validationInputs[:,0], validationOutputs, 'g^', label='Validation data (GDP)')     
plt.plot(trainInputs[:,1], trainOutputs, 'bo', label='Training data (Freedom)')   
plt.plot(validationInputs[:,1], validationOutputs, 'm^', label='Validation data (Freedom)')  
plt.title('Train and Validation Data')
plt.xlabel('Input Variables')
plt.ylabel('Happiness Score')
plt.legend()
plt.show()

# Model initialization and training
regressor = linear_model.LinearRegression()
regressor.fit(trainInputs, trainOutputs)

# Retrieve model parameters
w0, w1, w2 = regressor.intercept_, regressor.coef_[0], regressor.coef_[1]
print('The learnt model: f(x1, x2) = ', w0, ' + ', w1, ' * x1 + ', w2, ' * x2')

# Prepare synthetic data for plotting the learnt model
noOfPoints = 1000
x1_values = np.linspace(min(inputs1), max(inputs1), noOfPoints)
x2_values = np.linspace(min(inputs2), max(inputs2), noOfPoints)
X1, X2 = np.meshgrid(x1_values, x2_values)
Y = w0 + w1 * X1 + w2 * X2

# Plot the learnt model
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(trainInputs[:,0], trainInputs[:,1], trainOutputs, c='r', marker='o', label='Training Data')
ax.scatter(validationInputs[:,0], validationInputs[:,1], validationOutputs, c='g', marker='^', label='Validation Data')
ax.plot_surface(X1, X2, Y, alpha=0.5, cmap='viridis')
ax.set_xlabel('Economy..GDP.per.Capita.')
ax.set_ylabel('Freedom')
ax.set_zlabel('Happiness Score')
plt.title('Train Data, Validation Data, and the Learnt Model')
plt.legend()
plt.show()

# Use the trained model to predict new inputs
computedValidationOutputs = regressor.predict(validationInputs)

# Plot computed outputs vs real outputs
plt.plot(validationOutputs, computedValidationOutputs, 'yo')
plt.plot(validationOutputs, validationOutputs, 'g-')
plt.title('Computed Validation Outputs vs. Real Validation Outputs')
plt.xlabel('Real Validation Outputs')
plt.ylabel('Computed Validation Outputs')
plt.show()

# Compute prediction error
error = mean_squared_error(validationOutputs, computedValidationOutputs)
print("Normalizare")
print('Prediction error (tool): ', error)


error = mean_squared_error(validationOutputs, computedValidationOutputs)
print('prediction error (tool):  ', error)

print("Fara normalizare:")


print("prediction error (tool):  0.4218494215145122")
print("prediction error (tool):   0.4218494215145122")