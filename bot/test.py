import requests

url = "http://localhost:9000/api/r/hiphopheads"

print(requests.get(url).json())
