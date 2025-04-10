from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from azure.ai.vision.imageanalysis.models import VisualFeatures
from msrest.authentication import CognitiveServicesCredentials
from array import array
import os
from PIL import Image
import sys
import time
import matplotlib.pyplot as plt
from skimage import io
import numpy as np
import cv2
from math import sqrt
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score,f1_score

def setup():
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
    return computervision_client

# 1. Sa se foloseasca un algoritm de clasificare a imaginilor (etapa de inferenta/testare) si sa se stabileasca
# performanta acestui algoritm de clasificare binara (imagini cu biciclete vs. imagini fara biciclete).

def citireImagini():
    import cv2
    import os
    import matplotlib.pyplot as plt
    
    director_imagini = "D:/bikes"
    imagini = []
    
    for nume_fisier in os.listdir(director_imagini):
        cale_fisier = os.path.join(director_imagini, nume_fisier)
        
        # Verificăm dacă fișierul este o imagine
        if os.path.isfile(cale_fisier) and any(cale_fisier.endswith(extensie) for extensie in [".jpg", ".jpeg", ".png"]):
            # Adăugăm calea către imagine în listă
            imagini.append(cale_fisier)

    nr_imagini = len(imagini)
    nr_randuri = nr_imagini // 2 + nr_imagini % 2
    
    nr_coloane = 2
    figsize_per_image = 3
    fig, axes = plt.subplots(nr_randuri, nr_coloane, figsize=(nr_coloane * figsize_per_image, nr_randuri * figsize_per_image))
    
    for ax, imagine_path in zip(axes.flatten(), imagini):
        img = cv2.imread(imagine_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        ax.imshow(img_rgb)
        ax.axis('off')
    
    # Afișăm imaginea
    plt.tight_layout()
    plt.show()

citireImagini()

def evalClassificationV1(realLabels, computedLabels, labelNames):
    from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score
    
    cm = confusion_matrix(realLabels, computedLabels, labels = labelNames)
    acc = accuracy_score(realLabels, computedLabels)
    precision = precision_score(realLabels, computedLabels, average = None, labels = labelNames)
    recall = recall_score(realLabels, computedLabels, average = None, labels = labelNames)
    return acc, precision, recall 
    
def biciclete_in_imagini():

    computervision_client = setup()
    ground_truth = ["bike","bike","bike","bike","bike","bike","bike","bike","bike","bike","no-bike","no-bike","no-bike","no-bike","no-bike","no-bike","no-bike","no-bike","no-bike","no-bike"]
    prediction = []
    
    director_imagini = "D:/bikes"
    imagini = []
    nr_imagini_cu_bicicleta = 0
    nr_imagini_fara_bicicleta = 0
    
    for nume_fisier in os.listdir(director_imagini):
        cale_fisier = os.path.join(director_imagini, nume_fisier)
        
        # Verificăm dacă fișierul este o imagine
        if os.path.isfile(cale_fisier) and any(cale_fisier.endswith(extensie) for extensie in [".jpg", ".jpeg", ".png"]):
            # Adăugăm calea către imagine în listă
            imagini.append(cale_fisier)

    for imagine_path in imagini:
        img = open(imagine_path, "rb")
        result = computervision_client.analyze_image_in_stream(img, visual_features=[VisualFeatureTypes.objects])
        
        print(f"Analizând imaginea: {imagine_path}")
        found_bicycle = False
        
        for ob in result.objects:
            if ob.object_property == "bicycle":
                predicted_bicycle_bb = [ob.rectangle.x, ob.rectangle.y, ob.rectangle.x + ob.rectangle.w, ob.rectangle.y + ob.rectangle.h]
                found_bicycle = True
                break
       
        if found_bicycle:
            print("Bicicletă găsită în imagine.", predicted_bicycle_bb)
            nr_imagini_cu_bicicleta += 1  
            prediction.append("bike")
        else:
            print("Nu s-a găsit bicicletă în imagine.")
            nr_imagini_fara_bicicleta += 1
            prediction.append("no-bike")
            
    print()
    print("Total imagini biciclete prezise: ", nr_imagini_cu_bicicleta)
    print("Total imagini biciclete: ", 10)
    err = (sqrt((nr_imagini_cu_bicicleta - 10)**2))/2
    print("Eroare de: ", err)
    print()
    print("Total imagini fara biciclete prezise: ", nr_imagini_fara_bicicleta)
    print("Total imagini fara biciclete: ", 10)
    err = (sqrt((nr_imagini_fara_bicicleta - 10)**2))/2
    print("Eroare de: ", err)
    print()
    print("Ground truth:", ground_truth)
    print("Prediction: ", prediction)
    acc, prec, recall = evalClassificationV1(ground_truth, prediction, ['bike', 'no-bike'])
    #recall = true poz / (true poz + false neg)
    #precision = true poz / (true poz + false poz)
    print('acc: ', acc, ' precision: ', prec, ' recall: ', recall)
    
biciclete_in_imagini()