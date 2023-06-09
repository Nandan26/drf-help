import requests

endpoint = "http://localhost:8000/api/products/create/" 

data = {'title': 'Richie Poor',
    'price': 35.99
}
get_response = requests.post(endpoint, json = data) 

print(get_response.json())