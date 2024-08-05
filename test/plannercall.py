import requests


url = "https://graph.microsoft.com/v1.0/me"
response = requests.get(url)

response.text
