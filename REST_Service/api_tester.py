import sys
import requests, json
import cv2


# pass the image path as sys arg
image = sys.argv[1]

# convert image json accepted format
img = cv2.imread(image)

# encode image
_, img_encoded = cv2.imencode(".jpg", img)
data = img_encoded.tostring()
# prepare http request headers
content_type = "/image/jpeg"
headers = {"content-type": content_type}

# define url for service
url = "http://localhost:9999/api"


# send and get the reponse
response = requests.post(url=url, data=data, headers=headers)
print(json.loads(response.text))