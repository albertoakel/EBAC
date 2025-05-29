import requests
from bs4 import BeautifulSoup
import pandas as pd

# Cabeçalho HTTP adicionado para simular o acesso por um navegador
# Isso foi necessário porque sem o cabeçalho, o site retornava um HTML incompleto.
header = {
    "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}

print('REQUEST: ')
# Alteração: incluído o parâmetro `headers=header` na requisição para simular um navegador
response = requests.get('https://finance.yahoo.com/quote/%5EBVSP/history/', headers=header)
print(response.text[:600])

print('Beautiful: ')
soup = BeautifulSoup(response.text, features='html.parser')
print(soup.prettify()[:1000])

print('Pandas: ')
# Alteração: agora `pandas.read_html` usa o conteúdo HTML da resposta `response.text`
# antes, o pandas tentava acessar a URL diretamente (o que falhava sem o cabeçalho)
url_dados = pd.read_html(response.text)
print(url_dados[0].head(10))