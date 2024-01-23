import requests

url = "http://127.0.0.1:8083/2dto3d"

files = [('file', open("C:/Users/ming7/OneDrive/桌面/bird.png", 'rb'))]
data = {'master_id': '123456'}
response = requests.post(url, files=files, data=data)

print(response.json())
print("123")