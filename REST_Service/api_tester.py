import base64
import sys
import requests, json


# pass the image path as sys arg
image = sys.argv[1]

# convert image json accepted format


# prepare http request headers



# create json dump
url = "http://localhost:9999/api"
data = ""

# send and get the reponse
response = requests.post(url=url, data=data)
print(json.loads(response.text))