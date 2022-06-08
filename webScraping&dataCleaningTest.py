# -*- coding: utf-8 -*-
"""
Created on Mon May 16 17:44:29 2022

@author: Josias Gomez
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import re


links = []
pages = ['https://www.estadisticaciudad.gob.ar/eyc/?p=128836','https://www.estadisticaciudad.gob.ar/eyc/?p=128833']
for p in pages:
    page = requests.get(p)
    soup = bs(page.text)
    link = soup.find_all('a',class_='file-custom-field')
    url = str(link)
    url = re.findall(r'(?=http)[\S]*(?<=xlsx)', url)
    links.append(url)

df=pd.DataFrame()
for l in links:
    df1 = pd.read_excel(l[0])
    df1.drop(df1.index[[0,1,-3,-2,-1]],inplace=True)
    df1.set_axis(['producto','unidadMedida','marzo','abril'],axis=1,inplace=True)
    df = pd.concat([df,df1],axis=0)

df.reset_index(inplace=True)
df = df[['producto','abril']]

categorias = df[df['abril'].isna()]['producto']
indiceCat = list(categorias.index)
indicesProd = [i for i in df['producto'].index if i not in indiceCat]


rangos=[]
rangos = [list(range(indiceCat[i-1],indiceCat[i])) for i in range(len(indiceCat))]
rangos.append(list(range(indiceCat[-1],indicesProd[-1]+1)))
del rangos[0]

categorias = [[i] for i in categorias]
prueba = [rangos[i] + categorias[i] for i in range(len(categorias))]

data = []
df1 = pd.DataFrame()
df2 = pd.DataFrame()
for i in range(len(prueba)):
    for j in df[(df['producto'].index > prueba[i][0]) & (df['producto'].index <= prueba[i][-2])]['producto']:
        j = prueba[i][-1] + ' - ' + j
        data.append(j)

    df1 = pd.DataFrame(data)
    df2 = pd.concat([df2,df1]) 
    data = []

precios = df['abril']
precios.dropna(inplace=True)
precios.reset_index(inplace=True,drop=True)

df2.reset_index(inplace=True,drop=True)
df2 = pd.concat([df2,precios],axis=1)
print(df2)
