import csv
import os
import random
import math
from collections import defaultdict

class ManualANN:
    def __init__(self, input_size, hidden_size, output_size):
        self.weights1 = [[random.uniform(-0.5, 0.5) for _ in range(hidden_size)] 
                        for _ in range(input_size)]
        self.weights2 = [[random.uniform(-0.5, 0.5) for _ in range(output_size)] 
                        for _ in range(hidden_size)]
        self.bias1 = [0.0] * hidden_size
        self.bias2 = [0.0] * output_size

    def relu(self, x):
        return max(0, x)

    def softmax(self, x):
        exp = [math.exp(i) for i in x]
        sum_exp = sum(exp)
        return [i / sum_exp for i in exp]

    def forward(self, x):
        self.hidden = [0.0] * len(self.weights1[0])
        for j in range(len(self.weights1[0])):
            for i in range(len(x)):
                self.hidden[j] += x[i] * self.weights1[i][j]
            self.hidden[j] = self.relu(self.hidden[j] + self.bias1[j])

        self.output = [0.0] * len(self.weights2[0])
        for k in range(len(self.weights2[0])):
            for j in range(len(self.hidden)):
                self.output[k] += self.hidden[j] * self.weights2[j][k]
            self.output[k] += self.bias2[k]
        return self.softmax(self.output)

    def train(self, X, y, epochs=100, lr=0.01):
        for _ in range(epochs):
            for xi, target in zip(X, y):
                output = self.forward(xi)
                
                # Backward pass (simplificat)
                error = [output[k] - target[k] for k in range(len(output))]
                
                # Update weights2 și bias2
                for j in range(len(self.weights2)):
                    for k in range(len(self.weights2[0])):
                        self.weights2[j][k] -= lr * error[k] * self.hidden[j]
                    self.bias2[k] -= lr * error[k]
                
                # Update weights1 și bias1
                hidden_error = [0.0] * len(self.hidden)
                for j in range(len(self.hidden)):
                    for k in range(len(output)):
                        hidden_error[j] += error[k] * self.weights2[j][k]
                    hidden_error[j] *= 1 if self.hidden[j] > 0 else 0  # ReLU derivative

                for i in range(len(xi)):
                    for j in range(len(self.hidden)):
                        self.weights1[i][j] -= lr * hidden_error[j] * xi[i]
                    self.bias1[j] -= lr * hidden_error[j]

# --- Încărcare și preprocesare date ---
def load_data():
    crtDir = os.getcwd()
    fileName = os.path.join(crtDir, 'data', 'reviews_mixed.csv')
    texts, labels = [], []
    with open(fileName, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            texts.append(row[0])
            labels.append(row[1])
    return texts[:100], labels[:100] 

def preprocess(texts, labels):
    word_counts = defaultdict(int)
    for text in texts:
        for word in text.lower().split():
            word_counts[word] += 1
    vocab = sorted(word_counts.keys())[:500]  

    X = []
    for text in texts:
        features = [0] * len(vocab)
        for word in text.lower().split():
            if word in vocab:
                features[vocab.index(word)] += 1
        X.append(features)
    
    
    label_map = {label: idx for idx, label in enumerate(set(labels))}
    y = [[1 if i == label_map[label] else 0 for i in range(len(label_map))] 
         for label in labels]
    
    return X, y, vocab, label_map


texts, labels = load_data()
X, y, vocab, label_map = preprocess(texts, labels)
ann = ManualANN(input_size=len(vocab), hidden_size=32, output_size=len(label_map))
ann.train(X, y, epochs=50, lr=0.001)

fileName = os.path.join( 'data', 'reviews_mixed.csv')

input_text = fileName
input_vec = [0] * len(vocab)
for word in input_text.lower().split():
    if word in vocab:
        input_vec[vocab.index(word)] += 1
pred = ann.forward(input_vec)
predicted_label = list(label_map.keys())[list(label_map.values()).index(pred.index(max(pred)))]
print(f"Sentiment: {predicted_label} (Prob: {max(pred):.2f})")