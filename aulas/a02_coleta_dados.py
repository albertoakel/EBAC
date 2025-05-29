#https://python.org.br/web/


from bs4 import BeautifulSoup
import requests
url='https://python.org.br/web/'
#url='https://g1.globo.com/'
rqc= requests.get(url)  #chamado
extr=BeautifulSoup(rqc.text,features='html.parser') #extração



#exibir texto
# print(extr.text)
#print(extr.text.strip())

# Em html os títulos são organizados em tag h1,h2,h3. onde o número é relativo ao tamanho do texto no site.
# Atenção, os números em h1,h2,h3 não é relativo a alguma lista ou disposição no site!!

#listar( ou filtrar) pelas tag
p=0;h=0
for linha_texto in extr.find_all(['h2','p']):
    if linha_texto.name == 'h2':
        print('h2',linha_texto.text.strip())
        h+=1
    else:
        print('p',linha_texto.text.strip())
        p+=1
print(h,p)






