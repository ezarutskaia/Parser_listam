import pandas as pd
import re

df = pd.read_csv('df.csv', delimiter=',')

search1 = lambda s: s.lstrip("$")
df['price'] = df['price'].map(search1)

search2 = lambda x: x.split(',')
df['car'] = df['model'].map(search2)

print(df.head(5))