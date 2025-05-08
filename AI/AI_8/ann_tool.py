import csv
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.neural_network import MLPClassifier

# Încărcare date
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
    return texts[:500], labels[:500]  

texts, labels = load_data()

# Convertim etichetele în valori numerice
le = LabelEncoder()
y = le.fit_transform(labels)
print(y)

# Extragem caracteristici TF-IDF
vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(texts)

# Split date
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = MLPClassifier(max_iter=1000)
model.fit(X_train, y_train)

# Evaluare
y_pred = model.predict(X_test)
print(f"Acuratețe: {accuracy_score(y_test, y_pred):.2f}")

crtDir = os.getcwd()
fileName = os.path.join(crtDir, 'data', 'reviews_mixed.csv')

input_text = fileName
input_vec = vectorizer.transform([input_text])
pred = model.predict(input_vec)
print(f"Sentiment: {le.classes_[pred[0]]}")