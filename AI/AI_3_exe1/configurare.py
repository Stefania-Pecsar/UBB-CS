from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from array import array
import os
from PIL import Image,ImageDraw
import sys
import time
import os
import matplotlib.pyplot as plt

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

image_path = r"D:/test1.png"
#image_path = r"D:/test2.jpeg"

with open(image_path, "rb") as img:
    read_response = computervision_client.read_in_stream(
        image=img,
        mode="Printed",
        raw=True
    )


operation_id = read_response.headers['Operation-Location'].split('/')[-1]
while True:
    read_result = computervision_client.get_read_result(operation_id)
    if read_result.status not in ['notStarted', 'running']:
        break
    time.sleep(1)

# Print the detected text, line by line
result = []
if read_result.status == OperationStatusCodes.succeeded:
    for text_result in read_result.analyze_result.read_results:
        for line in text_result.lines:
            print(line.text)
            result.append(line.text)

print()

groundTruth = ["Succes in rezolvarea", "tEMELOR la", "LABORAtoaree de", "Inteligenta Artificiala!"]

# compute the performance
noOfCorrectLines = sum(i == j for i, j in zip(result, groundTruth))
print(noOfCorrectLines)

#1a

import pathlib

# Calea către fișierul cu imaginea
file_path = "D:/test1.png"
file_path = os.path.abspath(file_path)
# Convertirea căii către un URL local
print("URI-ul imaginii:", file_path)
file_url = pathlib.Path(file_path).as_uri()
print("URL-ul imaginii:", file_url)

print()

print("analyze_image_in_stream")
image_analysis = computervision_client.analyze_image_in_stream(open(file_path, "rb"), visual_features=[VisualFeatureTypes.tags])
for tag in image_analysis.tags:
    print(tag)
 
print()

print("Get subject domain list")
models = computervision_client.list_models()
for x in models.models_property:
    print(x)

print()

print("Analyze an image by domain")
domain = "landmarks"
language = "en"

with open(file_path, "rb") as image_stream:
    image_analysis = computervision_client.analyze_image_in_stream(image_stream, visual_features=[VisualFeatureTypes.tags])

# Afisarea etichetelor asociate imaginii
if image_analysis.tags:
    print("Tags:")
    for tag in image_analysis.tags:
        print(tag.name)
else:
    print("No tags found")

print()

print("Get text description of an image")
domain = "landmarks"
language = "en"
max_descriptions = 3

# Analiza imaginii utilizând fluxul binar al imaginii
with open(file_path, "rb") as image_stream:
    analysis = computervision_client.describe_image_in_stream(image_stream, max_descriptions, language)

# Afisarea descrierii textuale a imaginii
for caption in analysis.captions:
    print(caption.text)
    print(caption.confidence) #nivelul de incredere

print()

print("Get text from image")
img = img = open(file_path, "rb")

# SDK call
rawHttpResponse = computervision_client.read_in_stream(
    image=img,
    mode="Printed",
    raw=True
)

# Get ID from returned headers
operation_id = read_response.headers['Operation-Location'].split('/')[-1]
while True:
    read_result = computervision_client.get_read_result(operation_id)
    if read_result.status not in ['notStarted', 'running']:
        break
    time.sleep(1)


result = []
if read_result.status == OperationStatusCodes.succeeded:
    for text_result in read_result.analyze_result.read_results:
        for line in text_result.lines:
            print(line.text)
            result.append(line.text)
        
print("OK")

print()
cv_client = ImageAnalysisClient(
    endpoint=os.environ["VISION_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["VISION_KEY"])
)

with open(image_path, "rb") as image_file:
    image_data = image_file.read()

result = cv_client.analyze(
     image_data=image_data,
     visual_features=[VisualFeatures.READ]
 )

if result.read is not None:
     print("\nText:")

     # Prepare image for drawing
     image = Image.open("D:/test1.png")
     fig = plt.figure(figsize=(image.width/100, image.height/100))
     plt.axis('off')
     draw = ImageDraw.Draw(image)
     color = 'cyan'

     for line in result.read.blocks[0].lines:
         # Return the text detected in the image
         print(f"  {line.text}")    
            
         drawLinePolygon = True
            
         r = line.bounding_polygon
         bounding_polygon = ((r[0].x, r[0].y),(r[1].x, r[1].y),(r[2].x, r[2].y),(r[3].x, r[3].y))
         draw.polygon(bounding_polygon, outline=color, width=3)
         # Return the position bounding box around each line
            
            # Return each word detected in the image and the position bounding box around each word with the confidence level of each word
         for word in line.words:
             print(f"    {word.text}")
            # Draw word bounding box
             wr = word.bounding_polygon  
             word_bounding_box  = ((wr[0].x, wr[0].y), (wr[1].x, wr[1].y), (wr[2].x, wr[2].y), (wr[3].x, wr[3].y))
             draw.polygon(word_bounding_box, outline="red", width=1)
         # Return each word detected in the image and the position bounding box around each word with the confidence level of each word
            
            
         # Draw line bounding polygon
         #if drawLinePolygon:
           #  draw.polygon(bounding_polygon, outline=color, width=3)

     # Save image
     plt.imshow(image)
     plt.tight_layout(pad=0)
     outputfile = 'test1.png'
     fig.savefig(outputfile)
     print('\n  Results saved in', outputfile)
     print()


     