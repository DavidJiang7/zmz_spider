import requests
from datetime import datetime

url = 'http://www.google.com'
print("开始......")
print(datetime.now())
response = requests.get(url, timeout=10)
response.encoding ='utf-8'
html = response.text
print(html)