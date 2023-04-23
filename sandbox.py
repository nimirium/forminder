import requests
import json

url = 'https://thinking-tester-contact-list.herokuapp.com/users'
data = {
    "firstName": "Mishel",
    "lastName": "Tsesarsky",
    "email": "thefutureishere11@fake.com",
    "password": "1234567",
}

headers = {'Content-Type': 'application/json'}
page = requests.post(url, data=json.dumps(data), headers=headers)

print(page.status_code)
print(page.text)
