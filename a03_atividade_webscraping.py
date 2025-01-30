import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame

requests.packages.urllib3.disable_warnings()

url = 'https://books.toscrape.com/'
requisicao = requests.get(url)
requisicao.encoding = 'utf-8'

extracao = BeautifulSoup(requisicao.text, 'html.parser')

contar_livros = 0
catalogo = []


contar_livros = 0
catalogo = []
for artigo in extracao.find_all('article', class_='product_pod'):
    livro = {}
    contar_livros += 1
    for titulo in artigo.find_all('h3'):
        livro['Título'] = titulo.text.strip()
        #print('título:',titulo.text.strip())
    for preco in artigo.find_all('p',class_='price_color'):
        livro['Preço'] = preco.text.strip()

    catalogo.append(livro)
print('Total livros:', contar_livros)
df=DataFrame(catalogo)
print(df)

#     livro = {}
#     for ...:
#         titulo = ...
#         livro['Título'] = titulo
#     for ...:
#         preco = ...
#         livro['Preço'] = preco
#     catalogo.append(livro)
#
# print('Total livros:', contar_livros)
