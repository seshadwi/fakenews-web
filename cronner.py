import requests

req = requests.post('http://localhost:5000/api/syncnews')
print(req.text)