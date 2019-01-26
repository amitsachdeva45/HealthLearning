import http.client, urllib.request, urllib.parse, urllib.error, base64

headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': 'cfd53222bf084a459d88d3cca0fe522a',
}

params = urllib.parse.urlencode({
    # Request parameters
    'returnFaceId': 'false',
    'returnFaceRectangle': 'false',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'emotion'
})
image_path = "X:/priyanka/PriyankaPic.jpg"

# Read the image into a byte array
image_data = open(image_path, "rb").read()
try:
    conn = http.client.HTTPSConnection('canadacentral.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/detect?%s" % params, image_data, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
