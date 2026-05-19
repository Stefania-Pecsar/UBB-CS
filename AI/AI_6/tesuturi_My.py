import csv
import matplotlib.pyplot as plt 
import numpy as np 
import os
from math import sqrt
import random
from math import exp

def sigmoid(x):
    """Funcția sigmoidă."""
    return 1 / (1 + exp(-x))

class LogisticRegressionCustom:
    def __init__(self):
        self.intercept_ = 0.0
        self.coef_ = []

    def fit(self, x: list, y: list, learning_rate: float = 0.001, no_epochs: int = 1000):
        """Antrenează modelul de regresie logistică."""
        # Inițializează coeficienții aleatori
        self.coef_ = [random.random() for _ in range(len(x[0]) + 1)]
        
        # Aplică algoritmul gradient descent
        for _ in range(no_epochs):
            for i in range(len(x)):
                y_computed = sigmoid(self.eval(x[i], self.coef_))
                crt_error = y_computed - y[i]
                # Actualizează coeficienții
                for j in range(1, len(self.coef_)):
                    self.coef_[j] = self.coef_[j] - learning_rate * crt_error * x[i][j - 1]
                self.coef_[0] = self.coef_[0] - learning_rate * crt_error * 1

        # Salvează intercept-ul și coeficienții
        self.intercept_ = self.coef_[0]
        self.coef_ = self.coef_[1:]

    def eval(self, xi: list, coef: list):
        """Calculează valoarea estimată."""
        yi = coef[0]
        for j in range(len(xi)):
            yi += coef[j + 1] * xi[j]
        return yi

    def predict_one_sample(self, sample_features: list):
        """Predictia pentru un singur sample."""
        threshold = 0.5
        coefficients = [self.intercept_] + [c for c in self.coef_]
        computed_float_value = self.eval(sample_features, coefficients)
        computed01_value = sigmoid(computed_float_value)
        computed_label = 0 if computed01_value < threshold else 1
        return computed_label

    def predict(self, in_test):
        """Predictia pentru un set de teste."""
        computed_labels = [self.predict_one_sample(sample) for sample in in_test]
        return computed_labels
    
#conventie de date M = 1. B = 0
def loadDataMoreInputs(fileName, inputVariabNames, outputVariabName):
    def transform_output(output):
        return 1 if output == 'M' else 0

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
    outputs = [transform_output(data[i][selectedOutput]) for i in range(len(data))]
    
    return inputs, outputs

def plot3Ddata(x1Train, x2Train, yTrain, x1Model=None, x2Model=None, yModel=None, x1Test=None, x2Test=None, yTest=None, title=None):
    
    ax = plt.axes(projection='3d')
    
    if x1Train is not None:
        colors = ['g' if val == 0 else 'r' if val == 1 else 'b' for val in yTrain]
        ax.scatter(x1Train, x2Train, yTrain, c=colors, marker='o', label='Radius vs Texture')
    if x1Model is not None:
        ax.scatter(x1Model, x2Model, yModel, c='b', marker='o', label='learnt model')
    if x1Test is not None:
        ax.scatter(x1Test, x2Test, yTest, c='black', marker='^', label='test data')
    
    plt.title(title)
    plt.legend()
    plt.show()

def plot3DdataEstetic(x1Train, x2Train, yTrain, x1Model=None, x2Model=None, yModel=None, x1Test=None, x2Test=None, yTest=None, title=None):

    
    ax = plt.axes(projection='3d')
    
    if x1Train is not None:
        colors = ['g' if val == 0 else 'r' if val == 1 else 'b' for val in yTrain]
        ax.scatter(x1Train, x2Train, yTrain, c=colors, marker='o', label='Radius vs Texture')
    if x1Model is not None:
        ax.scatter(x1Model, x2Model, yModel, c='b', marker='o', label='learnt model')
    if x1Test is not None:
        ax.scatter(x1Test, x2Test, yTest, c='black', marker='^', label='test data')
    
    plt.title(title)

    plt.legend()
    plt.show()

def plot2Ddata(x, variableName):
    n, bins, patches = plt.hist(x, 10)
    plt.title('Histogram of ' + variableName)
    plt.show()

crtDir =  os.getcwd()
filePath = os.path.join(crtDir, 'D:/fac/AN 2/AI/AI_6/BreastCancer', 'wdbc.csv')

inputs, outputs = loadDataMoreInputs(filePath, ['texture1', 'radius1'], 'Diagnosis')

feature1 = [ex[0] for ex in inputs]
feature2 = [ex[1] for ex in inputs]

# plot the data histograms
# plot2Ddata(inputs[0], "texture1")
# plot2Ddata(inputs[1], "radius1")

# plot2Ddata(outputs, 'Diagnosis')

# check the liniarity (to check that a linear relationship exists between the dependent variable (y = happiness) and the independent variables (x1 = capita, x2 = freedom).)
# plot3DdataEstetic(feature1, feature2, outputs, [], [], [], [], [], [], 'texture1 vs radius1 vs Diagnosis')

np.random.seed(5)
indexes = [i for i in range(len(inputs))]
trainSample = np.random.choice(indexes, int(0.8 * len(inputs)), replace = False)
testSample = [i for i in indexes  if not i in trainSample]

trainInputs = [inputs[i] for i in trainSample]
trainOutputs = [outputs[i] for i in trainSample]
testInputs = [inputs[i] for i in testSample]
testOutputs = [outputs[i] for i in testSample]


feature1train = [ex[0] for ex in trainInputs]
feature2train = [ex[1] for ex in trainInputs]

feature1test = [ex[0] for ex in testInputs]
feature2test = [ex[1] for ex in testInputs]

# plot3Ddata(feature1train, feature2train, trainOutputs, None, None, None, feature1test, feature2test, testOutputs, "train and test data (after normalisation)")

# Definirea datelor de intrare și ieșire
# Dacă nu ai definit încă trainInputs, trainOutputs, testInputs și testOutputs, trebuie să le definești aici

# Antrenarea regresiei logistice personalizate
# Antrenarea regresiei logistice personalizate
model = LogisticRegressionCustom()
model.fit(trainInputs, trainOutputs)

# Evaluarea modelului personalizat pe datele de test
accuracy_custom = np.mean(model.predict(testInputs) == testOutputs)
print("Accuracy (Custom Logistic Regression):", accuracy_custom)

w0 = model.intercept_
w1, w2 = model.coef_
# Afișarea coeficienților și interceptării
print("Model coefficients (Custom Logistic Regression):")
print("f(x) =  1/ (1 + e^-z) where z = ", w0, ' + ', w1, ' * x1 + ', w2, ' * x2' )
print("tool")
print("f(x) =  1/ 1+ e^-z.......z=  -23.20486745717624  +  0.2448064130947617  * x1 +  1.2436777768597458  * x2")

trainInputs = np.array(trainInputs)
noOfPoints = 1000
xref1 = []
val = min(trainInputs[:, 0])
step1 = (max(trainInputs[:, 0]) - min(trainInputs[:, 0])) / noOfPoints
for _ in range(noOfPoints):
    xref1.append(val)
    val += step1

xref2 = []
val = min(trainInputs[:, 1])
step2 = (max(trainInputs[:, 1]) - min(trainInputs[:, 1])) / noOfPoints
for _ in range(noOfPoints):
    xref2.append(val)
    val += step2

yref = [1 / (1 + np.exp(-(w0 + w1 * el1 + w2 * el2))) for el1, el2 in zip(xref1, xref2)]
plot3Ddata(feature1train, feature2train, trainOutputs, xref1, xref2, yref, [], [], [], 'train data and the learnt model')

computedTestOutputs = model.predict(testInputs)

# plot3Ddata([], [], [], feature1test, feature2test, computedTestOutputs, feature1test, feature2test, testOutputs, 'predictions vs real test data')
error = 0.0
for t1, t2 in zip(computedTestOutputs, testOutputs):
    error += (t1 - t2) ** 2
error = error / len(testOutputs)

print("tool")
print("prediction error (manual):  0.19298245614035087")
print("prediction error (tool):    0.19298245614035092")
print("MyRegression")
print('prediction error (manual): ', error)

ec = 1 / (1 + np.exp(-(w0 + w1 * 10 + w2 * 18)))
print("Rez ec", ec)
if ec >= 0.5:
    print("Malign")
else:
    print("Benign ")