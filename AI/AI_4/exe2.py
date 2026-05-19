from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from array import array
import os
from PIL import Image, ImageDraw
import sys
import time
import pandas as pd
import matplotlib.patches as patches
from itertools import zip_longest
import unicodedata
from itertools import permutations
from math import sqrt
import matplotlib.pyplot as plt
import numpy as np
import sys
sys.stdout.reconfigure(encoding='utf-8')


# CERINTA:

#   2. Pentru imaginile care contin biciclete:
#           --> a. sa se localizeze automat bicicletele in aceste imagini si sa se evidentieze chenarele care incadreaza bicicletele
#           --> b. sa se eticheteze (fara ajutorul algoritmilor de AI) aceste imagini cu chenare care sa incadreze cat mai exact bicicletele. 
#               Care task dureaza mai mult (cel de la punctul a sau cel de la punctul b)?
#           --> c. sa se determine performanta algoritmului de la punctul a avand in vedere etichetarile realizate la punctul b (se vor folosi cel putin 2 metrici).



def authenticate():
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



"""
Detecteaza bicicletele dintr-o imagine folozind Azure Computer Vision (cu afisarea imaginii)

Date de intrare:
    image_path - string
    computervision_client - ComputerVisionClient

Date de iesire: tuple(has_bicycle, bicycle_location)
    has_bicycle - bool (True - daca bicicleta a fost gasita in imaginea, False - altfel)
    bicycle_location - BoundingRect

Complexitate timp: O(k), unde k - numarul de obiecte detectate in imagine
Complexitate spatiu: O(1)
"""
def detect_bicycle(image_path, computervision_client):
    with open(image_path, "rb") as img:
        result = computervision_client.analyze_image_in_stream(img, visual_features=[VisualFeatureTypes.objects])
        image = plt.imread(image_path)
        plt.imshow(image)
        for ob in result.objects:
            if ob.object_property == "bicycle":
                # Extrag coordonatele bounding box-ului
                x,y,w,h = ob.rectangle.x, ob.rectangle.y, ob.rectangle.w, ob.rectangle.h

                # Desenez boundin box-ul
                plt.gca().add_patch(plt.Rectangle((x, y), w, h, fill=False, edgecolor='red', linewidth=2))

                # Afisez imaginea cu bounding box-ul
                plt.show()
                return True, ob.rectangle

        return False, None



"""
Detecteaza bicicletele dintr-o imagine folozind Azure Computer Vision (fara afisare)

Date de intrare:
    image_path - string
    computervision_client - ComputerVisionClient

Date de iesire: tuple(has_bicycle, detected_boxes)
    has_bicycle - bool (True - daca bicicleta a fost gasita in imaginea, False - altfel)
    detected_boxes - list[BoundingRect]

Complexitate timp: O(k), unde k - numarul de obiecte detectate in imagine
Complexitate spatiu: O(k)
"""
def detect_bicycle2(image_path, computervision_client):
    with open(image_path, "rb") as img:
        result = computervision_client.analyze_image_in_stream(img, visual_features=[VisualFeatureTypes.objects])
        detected_boxes = []  # Lista pentru toate detectiile
        for ob in result.objects:
            if ob.object_property.lower() == "bicycle":
                detected_boxes.append(ob.rectangle)
        return (len(detected_boxes) > 0, detected_boxes)  # Returneaza lista



"""
Afiseaza bounding box-urile detectate (rosu) si manuale (albastru) pentru imaginile care contin biciclete

Date de intrare:
    image_dir - string
    csv_file - string
    computervision_client - ComputerVisionClient
    groundTruth - dictionar cu etichete binare pentru imagini

Date de iesire: -

Complexitate timp: O(m * (d + g)), unde m - numarul de imagini, d - numarul de detectii/imagine, g - numarul de boundin box-uri dn csv
Complexitate spatiu: O(1)
"""
def display_bounding_boxes(image_dir, csv_file, computervision_client, groundTruth):
    df = pd.read_csv(csv_file)

    for image_name in os.listdir(image_dir):
        if groundTruth[image_name] == 1:
            image_path = os.path.join(image_dir, image_name)

            with open(image_path, "rb") as img:
                result = computervision_client.analyze_image_in_stream(img, visual_features=[VisualFeatureTypes.objects])
                image = plt.imread(image_path)
                fix, ax = plt.subplots(1)
                ax.imshow(image)

                # Desenam chenarele detectate de AI in rosu
                for ob in result.objects:
                    if ob.object_property == "bicycle":
                        x, y, w, h = ob.rectangle.x, ob.rectangle.y, ob.rectangle.w, ob.rectangle.h
                        rect = patches.Rectangle((x, y), w, h, fill=False, edgecolor='red', linewidth=2, label="AI Detection")
                        ax.add_patch(rect)


                # Desenam chenarele din fisierul CSV in albastru
                if image_name in df['image_name'].values:
                    for _, row in df[df['image_name'] == image_name].iterrows():
                        x, y, w, h = row['bbox_x'], row['bbox_y'], row['bbox_width'], row['bbox_height']
                        rect = patches.Rectangle((x, y), w, h, fill=False, edgecolor='blue', linewidth=2, label="Manual Label")
                        ax.add_patch(rect)

                # Creez un dictionar pentru a pastra unica fiecare eticheta
                handles, labels = ax.get_legend_handles_labels()
                by_label = dict(zip(labels, handles))  # Elimin duplicatele

                plt.legend(by_label.values(), by_label.keys())  # Adaug doar etichetele unice
                plt.show()




"""
a. sa se localizeze automat bicicletele in aceste imagini si sa se evidentieze chenarele care incadreaza bicicletele
"""
def p2_a(computervision_client, images_folder):
    start_time = time.time()
    
    bicycles = []
    for image_name in os.listdir(images_folder):
        image_path = os.path.join(images_folder, image_name)
        has_bicycle, bicycle_location = detect_bicycle(image_path, computervision_client)
        bicycles.append((image_name, has_bicycle, bicycle_location))


    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Timp automat: {elapsed_time} secunde\n")

    



"""
Calculeaza Intersection over Union intre bounding box-uri
Date de intrare:
    boxA - BoundingRect (detectat de AI)
    boxB - tuple (manual din csv)

Date de iesire: float (intre 0 si 1)

Complexitate timp: O(1)
Complexitate spatiu: O(1)
"""
def IoU(boxA, boxB):
    xA, yA, wA, hA = boxA.x, boxA.y, boxA.w, boxA.h 
    xB, yB, wB, hB = boxB[0], boxB[1], boxB[2], boxB[3]

    x1 = max(xA, xB)
    y1 = max(yA, yB)
    x2 = min(xA + wA, xB + wB)
    y2 = min(yA + hA, yB + hB)

    inter_area = max(0, x2 - x1) * max(0, y2 - y1)
    union_area = (wA * hA) + (wB * hB) - inter_area
    
    return inter_area / union_area if union_area != 0 else 0



"""
Calculeaza Distance over Union intre bounding box-uri
Date de intrare:
    boxA - BoundingRect (detectat de AI)
    boxB - tuple (manual din csv)

Date de iesire: float (intre 0 si 1)

Complexitate timp: O(1)
Complexitate spatiu: O(1)
"""
def DIoU(boxA, boxB):
    iou = IoU(boxA, boxB)

    xA, yA, wA, hA = boxA.x, boxA.y, boxA.w, boxA.h  # Azure BoundingRect
    xB, yB, wB, hB = boxB[0], boxB[1], boxB[2], boxB[3]  # CSV ground truth

    centerA = (xA + wA/2, yA + hA/2)
    centerB = (xB + wB/2, yB + hB/2)

    # Distanta euclidiana intre centre
    d = sqrt((centerA[0] - centerB[0])**2 + (centerA[1] - centerB[1])**2)

    # Diagonala casutei care inconjoara ambele bounding box-uri
    c_x1 = min(xA, xB)
    c_y1 = min(yA, yB)
    c_x2 = max(xA + wA, xB + wB)
    c_y2 = max(yA + hA, yB + hB)
    c = sqrt((c_x2 - c_x1)*2 + (c_y2 - c_y1)*2)

    # Calcul DIoU
    iou = IoU(boxA, boxB)
    diou = iou - (d*2) / (c*2 + 1e-9)  # +1e-9 pentru a evita impartirea la 0
    return diou



"""
Calculeaza Complete over Union intre bounding box-uri
Date de intrare:
    boxA - BoundingRect (detectat de AI)
    boxB - tuple (manual din csv)

Date de iesire: float (intre 0 si 1)

Complexitate timp: O(1)
Complexitate spatiu: O(1)
"""
def CIoU(boxA, boxB):
    iou = IoU(boxA, boxB)
    diou = DIoU(boxA, boxB)

    wA, hA = boxA.w, boxA.h
    wB, hB = boxB[2], boxB[3]

    v = (4 / (np.pi ** 2)) * ((np.arctan(wB / hB) - np.arctan(wA / hA)) ** 2)
    alpha = v / (1 - iou + v)

    ciou = diou - alpha * v
    return ciou




"""
c. sa se determine performanta algoritmului de la punctul a avand in vedere etichetarile realizate la punctul b (se vor folosi cel putin 2 metrici).
"""
def p2_c(images_folder, real_bounding_boxes, computervision_client, groundTruth):
    df = pd.read_csv(real_bounding_boxes)

    iou_scores = []
    diou_scores = []
    ciou_scores = []
    y_true = []
    y_pred = []
    
    print("\n\n--- Metrici per imagine ---")
    for image_name in os.listdir(images_folder):
        if groundTruth.get(image_name, 0) == 1:
            image_path = os.path.join(images_folder, image_name)
            
            # Detectare biciclete cu Azure
            detected, detected_boxes = detect_bicycle2(image_path, computervision_client)
            
            # Citire bounding box-uri reale din CSV
            gt_boxes = df[df["image_name"] == image_name][["bbox_x", "bbox_y", "bbox_width", "bbox_height"]].values
            
            # Actualizare etichete pentru metrici de clasificare
            y_true.append(1)
            y_pred.append(1 if detected else 0)
            
            # Afisare metrici pentru imaginea curenta
            print(f"\nImagine: {image_name}")
            print(f"Detectat: {'Da' if detected else 'Nu'}")
            
            if detected:
                if len(gt_boxes) == 0:
                    print("EROARE: Nu există bounding box-uri în CSV!")
                    continue
                
                # Calcul metrici de localizare
                best_iou = 0.0
                best_diou = 0.0
                best_ciou = 0.0
                
                # Iterează prin toate detectiile si ground truth-urile
                for detected_box in detected_boxes:
                    for gt_box in gt_boxes:
                        iou = IoU(detected_box, gt_box)
                        diou = DIoU(detected_box, gt_box)
                        ciou = CIoU(detected_box, gt_box)
                        
                        if iou > best_iou:
                            best_iou = iou
                            best_diou = diou
                            best_ciou = ciou
                
                iou_scores.append(best_iou)
                diou_scores.append(best_diou)
                ciou_scores.append(best_ciou)
                
                print("="*50)
                print(f"Cea mai buna potrivire:")  # Pentru cazul in care imaginea are mai multe bounding box-uri
                print(f"- IoU: {best_iou:.4f}")
                print(f"- DIoU: {best_diou:.4f}")
                print(f"- CIoU: {best_ciou:.4f}")
                print("="*50)
                print("\n\n")
            else:
                print("Bicicleta nu a fost detectata (False Negative)")

    # Calcul metrici globale
    print("\n--- Metrici de localizare ---")
    print(f"IoU mediu: {np.mean(iou_scores) if iou_scores else 0:.4f}")
    print(f"DIoU mediu: {np.mean(diou_scores) if diou_scores else 0:.4f}")
    print(f"CIoU mediu: {np.mean(ciou_scores) if ciou_scores else 0:.4f}")
    print("\n\n")

    # Afisare metrici
    print("--- Metrici de clasificare ---")
    print(f"Precision: {precision_score(y_true, y_pred):.4f}")
    print(f"Recall: {recall_score(y_true, y_pred):.4f}")
    print(f"Accuracy: {accuracy_score(y_true, y_pred):.4f}")
    


def p2():
    computervision_client = authenticate()
    images_folder = "D:/bikes/"
    real_bounding_boxes = "D:/bounding_box.csv"

    groundTruth = {
        "bike1.jpg":1,
        "bike02.jpg":1,
        "bike03.jpg":1,
        "bike04.jpg":1,
        "bike05.jpg":1,
        "bike06.jpg":1,
        "bike07.jpg":1,
        "bike08.jpg":1,
        "bike09.jpg":1,
        "bike10.jpg":1,
        "traffic01.jpg": 0,
        "traffic02.jpg": 0,
        "traffic03.jpg": 0,
        "traffic04.jpg": 0,
        "traffic05.jpg": 0,
        "traffic06.jpg": 0,
        "traffic07.jpg": 0,
        "traffic08.jpg": 0,
        "traffic09.jpg": 0,
        "traffic10.jpg": 0
    }


    # a. sa se localizeze automat bicicletele in aceste imagini si sa se evidentieze chenarele care incadreaza bicicletele
    
    #p2_a(computervision_client, images_folder)
    

    # b. sa se eticheteze (fara ajutorul algoritmilor de AI) aceste imagini cu chenare care sa incadreze cat mai exact bicicletele. 
    # Care task dureaza mai mult (cel de la punctul a sau cel de la punctul b)?
    
    #display_bounding_boxes(images_folder, real_bounding_boxes, computervision_client, groundTruth)


    # c. sa se determine performanta algoritmului de la punctul a avand in vedere etichetarile realizate la punctul b (se vor folosi cel putin 2 metrici).
    p2_c(images_folder, real_bounding_boxes, computervision_client, groundTruth)





p2()