import requests

endpoint = "http://localhost:8000/api/products/5/update" 

data = {
    "title": "Reach dad , Poor dad",
    "price": 55.55
}
get_response = requests.put(endpoint, json = data) 

print(get_response.json())