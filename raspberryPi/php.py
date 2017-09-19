import requests

r = requests.get('http://133.130.99.167/mimamo/public/searchImage')
print(r.status_code)