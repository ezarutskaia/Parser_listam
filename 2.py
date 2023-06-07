import pandas as pd
import re

df = pd.read_csv('df.csv', delimiter=',')

search = lambda s: s.lstrip("$")
df['price'] = df['price'].map(search)

expanded = df['model'].str.split(pat=',', n=3, expand=True)
df['car'] = expanded[0]
df['eng_cap'] = expanded[1]
df['year'] = expanded[2]

expanded1 = df['mileage'].str.split(pat=',', n=5, expand=True)
df['1000*km'] = expanded1[2]
df['si'] = expanded1[3]
df['fuel'] = expanded1[4]

df.drop(['model', 'mileage'], axis= 1 , inplace= True )

print(df.head(10))