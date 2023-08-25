import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import math

url = 'https://www.kabum.com.br/gamer/simuladores/fly-simulator'

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
    Chrome/111.0.0.0 Safari/537.36'}
site = requests.get(url,headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')
qtd_itens=soup.find('div',id='listingCount').get_text().strip()

index = qtd_itens.find(' ')
qtd = qtd_itens[:index]
print(qtd)

ultima_pagina = math.ceil(int(qtd)/20)
print(ultima_pagina)

series_produtos = {'marca':[],'preço':[]}

for i in range(1,ultima_pagina+1):
    url_pag = f'https://www.kabum.com.br/gamer/simuladores/fly-simulator?page_number={i}&page_size=20&facet_filters=&sort=most_searched'
   # url_pag = f'https://www.kabum.com.br/gamer/acessorios-gamer/joystick?page_number=&page_size=20&facet_filters=&sort=most_searched'
    site = requests.get(url_pag,headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    produtos = soup.find_all('div', class_=re.compile('productCard'))
    
    
    for produto in produtos:
        marca = produto.find('span', class_=re.compile('nameCard')).get_text().strip()
        preco = produto.find('span', class_=re.compile('priceCard')).get_text().strip()
        
        series_produtos['marca'].append(marca)
        series_produtos['preço'].append(preco)
        
df = pd.DataFrame(series_produtos)

df.to_csv('.\joy.csv')