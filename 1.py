import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
from mysql.connector import connect, Error
import numpy
import datetime
from datetime import date
import math
import matplotlib.pyplot as plt

headers = {
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0'
}
cookes = {
    'lang':	"1"
}

df = pd.DataFrame(columns=['price', 'model', 'mileage'])

URL_TEMPLATE1 = "https://www.list.am/category/23"
URL_TEMPLATE2 = "?n=0&bid=0&price1=&price2=11000&crc=&_a27=0&_a2_1=2007&_a2_2=&_a15=0&_a28_1=&_a28_2=&_a13=2&_a23=0&_a1_1=&_a1_2=150000&_a109=0&_a43=1&_a16=1&_a17=0&_a22=0&_a105=0&_a106=0&_a102=0&_a103=0&_a104=0"
for n in range(5):
    if n == 1:
        URL_PAGE = ''
    else:
        URL_PAGE = '/' + str(n)
    URL_TEMPLATE = URL_TEMPLATE1 + URL_PAGE + URL_TEMPLATE2
    page = requests.get(URL_TEMPLATE, headers=headers, cookies=cookes)
    soup = bs(page.text, "html.parser")
    groups = soup.find_all('div', class_='gl')
    for group in groups:
        cars = group.find_all('a')
        for car in cars:
            price = car.find_all('div', class_='p')[0]
            model = car.find_all('div', class_='l')[0]
            mileage = car.find_all('div', class_='at')[0]
            df.loc[ len(df.index )] = [price.text, model.text, mileage.text]
    #print(df)

search1 = lambda s: s.lstrip("$")
df['price'] = df['price'].map(search1)

expanded = df['model'].str.split(pat=',', expand=True)
df['car'] = expanded[0]
df['eng_cap'] = expanded[1]
df['year'] = expanded[2]

expanded0 = df['car'].str.split(pat=' ', expand=True)
df['brand'] = expanded0[0]

expanded1 = df['mileage'].str.split(pat=',', n=5, expand=True)
df['1000*km'] = expanded1[2]
df['si'] = expanded1[3]
df['fuel'] = expanded1[4]

expanded2 = df['si'].str.split(n=2, expand=True)
df['unit'] = expanded2[1]

#print(df)

for ind in df.index:
    if df['unit'][ind] == 'миль':
        df['1000*km'][ind] = int(int(df['1000*km'][ind]) * 1.6)
        #print(type(df['1000*km'][ind]))

search2 = lambda x: x.rstrip(" л.")
df['eng_cap'] = df['eng_cap'].map(search2)
search3 = lambda x:  str(x).rstrip(" г.") if x else 0
df['year'] = df['year'].map(search3)

df.drop(['model', 'mileage', 'si', 'unit'], axis= 1 , inplace= True )


search4 = lambda x: x if re.search(r"\d{4}", str(x)) else 0
df['year'] = df['year'].map(search4)

df = df[(df['fuel'] == ' Бензин')]
search5 = lambda s: s.strip()
df['fuel'] = df['fuel'].map(search5)

df['price'] = df['price'].str.replace(',', '')
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['eng_cap'] = pd.to_numeric(df['eng_cap'], errors='coerce')
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df['1000*km'] = pd.to_numeric(df['1000*km'], errors='coerce')

search6 = lambda x: 0 if math.isnan(x) else x
df['eng_cap'] = df['eng_cap'].map(search6)

df = df[['price', 'brand', 'car', 'eng_cap', 'year', '1000*km', 'fuel']]

#print(df.head(10))

try:
    with connect(
        host="localhost",
        user="lenochka",
        password="popstvuet",
        database="docker_cars",
        port="4306",
    ) as connection:

        with connection.cursor(buffered=True) as cursor:
            for ind in df.index:
                query = "INSERT INTO ArmenCar (price, brand, car, eng_cap, year, mileage, fuel, created) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(query, (df['price'][ind].tolist(), df['brand'][ind], df['car'][ind], df['eng_cap'][ind].tolist(), df['year'][ind].tolist(), df['1000*km'][ind].tolist(), df['fuel'][ind], date.today().strftime('%d.%m') ))
                connection.commit()
                # , brand, car, eng_cap, year, mileage, fuel
                # , df['brand'][ind], df['car'][ind], df['eng_cap'][ind], df['year'][ind], df['1000*km'][ind], df['fuel'][ind]

except Error as e:
    print('Error:',e)

#df.to_sql(con=sqlalchemy.engine.Connection, name='table_name_for_df', if_exists='replace', flavor='mysql')

#print(df.info())

df = df[df['year'] > 2000]
n1 = df[df['brand'] == 'Hyundai']
n2 = df[df['brand'] == 'Kia']
n3 = df[df['brand'] == 'Mazda']

plt.subplot(221)
plt.scatter(df['year'], df['price'])
plt.xlabel('Год')
plt.ylabel('Цена, $')
plt.subplot(222)
plt.scatter(n1['year'], n1['price'])
plt.xlabel('Год')
plt.ylabel('Цена, $')
plt.legend('hyundai', loc=1)
plt.subplot(223)
plt.scatter(n2['year'], n2['price'])
plt.xlabel('Год')
plt.ylabel('Цена, $')
plt.legend('kia', loc=1)
plt.subplot(224)
plt.scatter(n3['year'], n3['price'])
plt.xlabel('Год')
plt.ylabel('Цена, $')
plt.legend('mazda', loc=1)
plt.show()

plt.subplot(221)
plt.scatter(df['1000*km'], df['price'])
plt.xlabel('Пробег, 1000км')
plt.ylabel('Цена, $')
plt.subplot(222)
plt.scatter(n1['1000*km'], n1['price'])
plt.xlabel('Пробег, 1000км')
plt.ylabel('Цена, $')
plt.legend('hyundai', loc=4)
plt.subplot(223)
plt.scatter(n2['1000*km'], n2['price'])
plt.xlabel('Пробег, 1000км')
plt.ylabel('Цена, $')
plt.legend('kia', loc=4)
plt.subplot(224)
plt.scatter(n3['1000*km'], n3['price'])
plt.xlabel('Пробег, 1000км')
plt.ylabel('Цена, $')
plt.legend('mazda', loc=4)
plt.show()

#print(hyundai.head(5))