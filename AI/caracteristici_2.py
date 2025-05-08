# incorporari custom
import numpy as np
import csv
import os
import spacy
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.metrics import classification_report

def load_data():
    """Încarcă datele din fișierul CSV"""
    crtDir = os.getcwd()
    fileName = os.path.join(crtDir, 'data', 'reviews_mixed.csv')
    
    inputs = []
    outputs = []
    
    with open(fileName, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:  # Ignoră header-ul
                dataNames = row  
            else:
                if len(row) >= 2:
                    inputs.append(row[0])
                    outputs.append(row[1])
            line_count += 1
    
    return inputs[:100], outputs[:100]

def extract_features(texts):
    """Extrage caracteristici custom din texte"""
    nlp = spacy.load("en_core_web_sm")
    features = []
    
    for text in texts:
        doc = nlp(text)
        
        # Caracteristici statistice
        word_count = len(text.split())
        char_count = len(text)
        avg_word_length = np.mean([len(word) for word in text.split()]) if word_count > 0 else 0
        exclamation = int('!' in text)
        question = int('?' in text)
        
        # Caracteristici lingvistice
        noun_count = sum(1 for token in doc if token.pos_ == "NOUN")
        adj_count = sum(1 for token in doc if token.pos_ == "ADJ")
        verb_count = sum(1 for token in doc if token.pos_ == "VERB")
        
        # Polaritate (opțional, doar dacă ai activ spacytextblob)
        polarity = doc._.polarity if doc.has_extension("polarity") else 0

        # Combina toate caracteristicile
        features.append([
            word_count,
            char_count,
            avg_word_length,
            exclamation,
            question,
            noun_count,
            adj_count,
            verb_count,
            polarity
        ])
    
    return np.array(features)


inputs, outputs = load_data()
print("Primele 2 recenzii:", inputs[:2])
print("Etichete unice:", list(set(outputs)))


print("\nExtragere caracteristici...")
X = extract_features(inputs)
print(X)

encoder = LabelEncoder()
y = encoder.fit_transform(outputs)


X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nAntrenare model...")
classifier = SVC(kernel='linear')
classifier.fit(X_train, y_train)


y_pred = classifier.predict(X_test)
print("\nRaport de clasificare:")
print(classification_report(y_test, y_pred, target_names=encoder.classes_))

print("\nTestare pe recenzii reale:")
for idx in range(len(X_test)):
    features = X_test[idx].reshape(1, -1)  
    prediction = classifier.predict(features)[0]
    print(f"\nText: '{inputs[idx]}'")
    print(f"Etichetă reală: {encoder.inverse_transform([y_test[idx]])[0]}")
    print(f"Predicție model: {encoder.inverse_transform([prediction])[0]}")
