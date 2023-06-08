import pandas as pd
import re

df = pd.read_csv('df.csv', delimiter=',')

search1 = lambda s: s.lstrip("$")
df['price'] = df['price'].map(search1)

expanded = df['model'].str.split(pat=',', n=3, expand=True)
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

for ind in df.index:
    if df['unit'][ind] == 'миль':
        df['1000*km'][ind] = int(int(df['1000*km'][ind]) * 1.6)
        #print(type(df['1000*km'][ind]))

search2 = lambda x: x.rstrip(" л.")
df['eng_cap'] = df['eng_cap'].map(search2)
search3 = lambda x: x.rstrip(" г.")
df['year'] = df['year'].map(search3)

df.drop(['model', 'mileage', 'si', 'unit'], axis= 1 , inplace= True )


search4 = lambda x: x if re.search(r"\d{4}", x) else 0
df['year'] = df['year'].map(search4)

df = df[(df['fuel'] == ' Бензин')]
search5 = lambda s: s.strip()
df['fuel'] = df['fuel'].map(search5)

df['price'] = df['price'].str.replace(',', '')
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['eng_cap'] = pd.to_numeric(df['eng_cap'], errors='coerce')
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df['1000*km'] = pd.to_numeric(df['1000*km'], errors='coerce')

df = df[['price', 'brand', 'car', 'eng_cap', 'year', '1000*km', 'fuel']]

print(df.head(10))