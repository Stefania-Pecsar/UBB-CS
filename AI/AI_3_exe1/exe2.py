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
import io

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

image_path = r"D:/test2.jpeg"
with open(image_path, "rb") as image_file:
    image_data = image_file.read()

result = cv_client.analyze(
    image_data=image_data,
    visual_features=[VisualFeatures.READ]
)

#2.calitatea localizarii corecte a textului in imagine

resultRead=""
if result.read is not None:
    print("\nText")

    #pregatire pentru desenare
    image = Image.open("D:/test2.jpeg")
    fig = plt.figure(figsize=(image.width/100, image.height/100))
    plt.axis('off')
    draw = ImageDraw.Draw(image)
    color = 'cyan'

    for line in result.read.blocks[0].lines:
        #afisare text detectat
        print(f"  {line.text}")  
        resultRead+=str(line.text)+" "
        drawLinePolygon = True
        #coordonatele poligonului pentru linia detectata
        r = line.bounding_polygon
        bounding_polygon = ((r[0].x, r[0].y),(r[1].x, r[1].y),(r[2].x, r[2].y),(r[3].x, r[3].y))
        print("Pentru linii",bounding_polygon)
        draw.polygon(bounding_polygon,outline="red",width=3)

        ground_Truth = ((80, 304), (1342, 304), (1343, 453), (80, 464))
        draw.polygon(ground_Truth, outline="blue", width=2)

        ground_Truth = ((128, 594), (1042, 583), (1043, 712), (128, 723))
        draw.polygon(ground_Truth, outline="blue", width=2)

        ground_Truth = ((78, 912), (1016, 912), (1015, 1037), (76, 1020))
        draw.polygon(ground_Truth, outline="blue", width=2)

        ground_Truth = ((105, 1130), (1455, 1156), (1454, 1291), (102, 1260))
        draw.polygon(ground_Truth, outline="blue", width=2)

        #Desenare casete pentru fiecare cuvant
        for word in line.words:
            #print(f"    {word.text}")
            #caseta
            wr = word.bounding_polygon
            word_bounding_box  = ((wr[0].x, wr[0].y), (wr[1].x, wr[1].y), (wr[2].x, wr[2].y), (wr[3].x, wr[3].y))
            print("Pentru cuvinte", word_bounding_box)
            draw.polygon(word_bounding_box,outline="green",width=3)  



def iou(boxA, boxB):
    xA = max(boxA[0][0], boxB[0][0])
    yA = max(boxA[0][1], boxB[0][1])
    xB = min(boxA[2][0], boxB[2][0])
    yB = min(boxA[2][1], boxB[2][1])
    
    interWidth = max(0, xB - xA)
    interHeight = max(0, yB - yA)
    interArea = interWidth * interHeight

    if interArea == 0:
        return 0.0
    
    boxAArea = (boxA[2][0] - boxA[0][0]) * (boxA[2][1] - boxA[0][1])
    boxBArea = (boxB[2][0] - boxB[0][0]) * (boxB[2][1] - boxB[0][1])
    
    return interArea / float(boxAArea + boxBArea - interArea)


iou_value = iou(ground_Truth,word_bounding_box)
print("Eroare", iou_value)

    # Save image
plt.imshow(image)
plt.tight_layout(pad=0)
outputfile = 'test2_outline.jpg'
fig.savefig(outputfile)
print('\n Results in',outputfile)
print(resultRead)