import requests


from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import date

link1='https://www.terra.com.br/esportes/futebol/brasileiro-serie-a/tabela/'
link2='https://onefootball.com/en/competition/brasileirao-betano-16/table'

# df= pd.read_html(link1)
# #informações de coluna( 4 pontução)
# print(df[0].iloc[:,4])
# #informação de uma linha
# print(df[0].loc[4])
# #informacao time
# print(df[0].iloc[4,2])
# #situação na rodada
# print(df[0].iloc[4,3])

rqc = requests.get(link2)  ##call
extr=BeautifulSoup(rqc.text,features='html.parser') #extração

print(extr.text.strip())

a=0
p=a
for linha_texto in extr.find_all(['a']):
    #print('a---',a,linha_texto.text.strip())
    if a==14:
        bota=linha_texto.text.strip()
    a+=1

print(bota)

k=re.findall(r'\d+',bota)
print(k)
if re.search(p, bota) is not None:
    for catch in re.finditer(p, bota):
        print(catch[0])


# p=0;h=0
# for linha_texto in extr.find_all(['h2','p']):
#     if linha_texto.name == 'h2':
#         #print('h2',linha_texto.text.strip())
#         h+=1
#     else:
#         print('p',linha_texto.text.strip())
#         p+=1
# #print(h,p)