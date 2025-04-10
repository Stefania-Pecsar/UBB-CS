from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
import matplotlib.pyplot as plt
from array import array
import os
from PIL import Image, ImageDraw
import sys
import time
import Levenshtein
import jellyfish

os.environ["VISION_KEY"] ="FL6Gs066sjFiR1h5kmMLTt6jhm8B2mvRWkhJU8usTBRwr1KNaojhJQQJ99BCACPV0roXJ3w3AAAFACOGdm7g"
os.environ["VISION_ENDPOINT"] =  "https://aistefaniapecsar.cognitiveservices.azure.com/"
'''
Authenticate
Authenticates your credentials and creates a client.
'''

subscription_key = os.environ["VISION_KEY"]
endpoint = os.environ["VISION_ENDPOINT"]
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
'''
END - Authenticate
'''

cv_client = ImageAnalysisClient(
     endpoint=endpoint,
     credential=AzureKeyCredential(subscription_key)
 )

# Citirea imaginii
image_path = r"D:/test2.jpeg"
with open(image_path, "rb") as image_file:
    image_data = image_file.read()

# Analiza imagini
result = cv_client.analyze(
     image_data=image_data,
     visual_features=[VisualFeatures.READ] # specificare extragere text
 )

resultRead = ""
if result.read is not None:
    print("\nText:")

    image = Image.open("D:/test2.jpeg")

    for line in result.read.blocks[0].lines:
        #afisare text detectat
        print(f"  {line.text}")    
        resultRead += str(line.text)+" "
 
        for word in line.words:
            print(f"    {word.text}")
          
    print(resultRead)

#1. calitatea procesului de recunoastere a textului, atat la nivel de caracter, cat si la nivel de cuvant
#a. prin folosirea unei metrici de distanta sau
#b. prin folosirea mai multor metrici de distanta.

print()

print(resultRead)
#lista cuvinte detectate
result_cuvinte_FP = resultRead.split()
result_cuvinte = resultRead.split()

#modificare manuală a unor cuvinte detectate
#se elimină două cuvinte și se înlocuiește cu varianta corectată

del result_cuvinte[5]
del result_cuvinte[5]
result_cuvinte.insert(5,"LABORA toarele")
print(result_cuvinte)
#conversie lista in string
result_cuvinteCP = " ".join(result_cuvinte)
print(result_cuvinteCP)

print()

#rezultatul asteptat pt evaluare
resultat_asteptat = "Succes în rezolvarea tEMELOR la LABORAtoarele de Inteligență Artificială!"
resultat_asteptat_cuvinte = resultat_asteptat.split()

#calculare distanta Levensthein intre textul detectat si cel asteptat
cuvant_distantaFP = [Levenshtein.distance(cuvant_asteptat, cuvant_de_recunoscut) for cuvant_asteptat, cuvant_de_recunoscut in zip(resultat_asteptat_cuvinte, result_cuvinte_FP)]
cuvant_distanta = [Levenshtein.distance(cuvant_asteptat, cuvant_de_recunoscut) for cuvant_asteptat, cuvant_de_recunoscut in zip(resultat_asteptat_cuvinte, result_cuvinte)]  
nivel_caracter = Levenshtein.distance(resultat_asteptat, resultRead)


print("a. prin folosirea unei metrici de distanta")
print()
print("Inainte de prelucrarea output:")
print("Prin Levenshtein cuvinte",cuvant_distantaFP)
print("Prin Levenshtein caracter",nivel_caracter)
print("Dupa prelucrarea output:")
print("Prin Levenshtein cuvinte",cuvant_distanta)
print("Prin Levenshtein caracter",nivel_caracter)

print()

#calcul distanta Hamming

print("b. prin folosirea mai multor metrici de distanta.")
print()
distanta_cuvinte = 0
for i in range(len(resultat_asteptat)):
        # Incrementăm distanța dacă caracterele de pe aceeași poziție sunt diferite
    if result_cuvinteCP[i] != resultat_asteptat[i]:
            distanta_cuvinte += 1

distanta_caracter = 0
for linie_gen, linie_asteptata in zip(result_cuvinteCP, resultat_asteptat):
    for car_gen, car_asteptat in zip(linie_gen, linie_asteptata):
        distanta_caracter += car_gen != car_asteptat
        
print("Rezultat asteptat")
print(resultat_asteptat)
print("Rezultat generat")
print(result_cuvinteCP)
print("Prin Hamming cuvinte",distanta_cuvinte)
print("Prin Hamming caracter",distanta_caracter)

print()

#calculul similaritatii Jaro-Winkler
distanta_jaro_winkler = jellyfish.jaro_winkler_similarity(resultat_asteptat, resultRead)

print("Rezultat asteptat")
print(resultat_asteptat)
print("Rezultat generat")
print(resultRead)
print("Similaritate Jaro-Winkler ",distanta_jaro_winkler)

print()

#calcul scor clongest common subsequence
n = len(resultRead)
m = len(resultat_asteptat)
scores = [[0] * m for _ in range(n)]
for i in range(n):
    for j in range(m):
        str1 = resultRead[i]
        str2 = resultat_asteptat[j]
        if len(str1) != len(str2):
            scores[i][j] = float('inf')  #NU se poate calcula distanța Levenshtein
        else:
            score = sum(Levenshtein.distance(c1, c2) for c1, c2 in zip(str1, str2))
            scores[i][j] = score
print("Rezultat asteptat")
print(resultat_asteptat)
print("Rezultat generat")
print(resultRead)
print("Nivel Longest common subsequence",score)