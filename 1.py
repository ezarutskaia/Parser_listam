import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

URL_TEMPLATE = "https://www.list.am/category/23?n=0&bid=0&price1=&price2=11000&crc=&_a27=0&_a2_1=2007&_a2_2=&_a15=0&_a28_1=&_a28_2=&_a13=2&_a23=0&_a1_1=&_a1_2=150000&_a109=0&_a43=1&_a16=1&_a17=0&_a22=0&_a105=0&_a106=0&_a102=0&_a103=0&_a104=0"
headers = {
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0'
}
cookes = {
    'lang':	"1"
}
page = requests.get(URL_TEMPLATE, headers=headers, cookies=cookes)

soup = bs(page.text, "html.parser")
groups = soup.find_all('div', class_='gl')
for group in groups:
    cars = group.find_all('a')
    for car in cars:
        price = car.find_all('div', class_='p')[0].text
        print(price)