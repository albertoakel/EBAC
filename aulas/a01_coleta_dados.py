from bs4 import BeautifulSoup
import pandas as pd
from datetime import date
import requests



link1 = 'https://www.infomoney.com.br/cotacoes/b3/indice/ibovespa/historico/'
link2='https://www.terra.com.br/esportes/futebol/brasileiro-serie-b/tabela/'
header = {
    "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}
response = requests.get(link1, headers=header)

soup = BeautifulSoup(response.text, features='html.parser')
print(soup.prettify()[:1000])

print('Pandas: ')
# Alteração: agora `pandas.read_html` usa o conteúdo HTML da resposta `response.text`
# antes, o pandas tentava acessar a URL diretamente (o que falhava sem o cabeçalho)
url_dados = pd.read_html(response.text)
print(url_dados[0].head(2))

# print('REQUESTS')
# print(site.text[:600])
# print('BEAUTFULSOUP')
# soup = BeautifulSoup(site.text,features='html.parser')
# print(soup.prettify()[:1000])

# url_dados = pd.read_html(link1,attrs = {'id':
# 'quotes_history'})
# print('PANDAS')
# print(url_dados)
# #print(url_dados[0].head(10))

