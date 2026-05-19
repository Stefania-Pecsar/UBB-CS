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
from PIL import Image, ImageDraw, ImageFilter
import sys
import time
import os
import textdistance
import Levenshtein
import tempfile
import io

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

#incarcare si citire imagine
image_path = r"D:/test2.jpeg"
with open(image_path, "rb") as image_file:
    image_data = image_file.read()

#3.posibilitati de imbunatatire a recunoasterii textului

#lista asteptata ca rezultat
rezultat_asteptat = ["Succes in rezolvarea", "tEMELOR la", "LABORAtoaree de", "Inteligenta Artificiala!"]

#preluare si extragere text
def preluare_imagine(img):
    computervision_client = setup()
    read_response = computervision_client.read_in_stream(
        image=img,
        mode="Printed",
        raw=True
    )
    #print(read_response.as_dict())

    operation_id=read_response.headers['Operation-Location'].split('/')[-1]

    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted','running']:
            break
        time.sleep(1)

    # Print the detected text, line by line
    resultRead=""
    resultLinii = []
    resultCuvinte = []

    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                resultLinii.append(line.text)
                resultRead += str(line.text)
                for word in line.words:
                    resultCuvinte.append(word.text)

    print(resultRead)
    print(resultLinii)
    print(resultCuvinte)
    return resultLinii

def distantaJaroWinkler(rezultat_asteptat,resultRead):
    distanta_jaro_winkler =0
    for linie_generata,linie_asteptata in zip(resultRead,rezultat_asteptat):
        distanta_jaro_winkler += textdistance.jaro_winkler.normalized_similarity(linie_generata, linie_asteptata)
    return distanta_jaro_winkler / len(rezultat_asteptat)

def distantaLevenshtein(rezultat_asteptat,resultRead):
    nivel_caracter = Levenshtein.distance(rezultat_asteptat, resultRead)
    return nivel_caracter

def test_intput(imagine_prelucrata):
    plt.imshow(imagine_prelucrata)
    plt.show()
    image_bytes = io.BytesIO()
    imagine_prelucrata.save(image_bytes, format='JPEG')
    image_bytes.seek(0)
    image_buffered_reader = io.BufferedReader(image_bytes)
    
    R_R = preluare_imagine(image_buffered_reader)
    print(R_R)
    print(distantaJaroWinkler(rezultat_asteptat, R_R))
    print(distantaLevenshtein(rezultat_asteptat, R_R))


# Prelucrarea imaginii și aplicarea diferitelor filtre

imagine = Image.open("D:/test2.jpeg")
imagine_procesata = imagine.resize((600, 800))
imagine_procesata_COUNTOUR = imagine_procesata.filter(ImageFilter.CONTOUR)
plt.imshow(imagine_procesata_COUNTOUR)

print()

test_intput(imagine_procesata_COUNTOUR)

print()

imagine_procesata_2 = imagine.resize((600, 800))
imagine_procesata_2 = imagine_procesata_2.filter(ImageFilter.FIND_EDGES)
test_intput(imagine_procesata_2)

print()

imagine_procesata_3 = imagine.resize((600, 800))
imagine_procesata_3 = imagine_procesata_2.filter(ImageFilter.CONTOUR)
imagine_procesata_3 = imagine_procesata_2.filter(ImageFilter.EDGE_ENHANCE)
test_intput(imagine_procesata_3)