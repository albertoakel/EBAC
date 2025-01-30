
import pandas as pd
from pandas import DataFrame

#listas
lista_nome=['Ana', 'Marcos', 'Carlos']

dic_pessoa={'nome': 'Ana',
            'Idade':20,
            'cidade':'São paulo'}

dados=[
    {'nome': 'Ana','Idade':20,'cidade':'São paulo'},
    {'nome': 'Marcos', 'Idade': 34, 'cidade': 'São Jósé'},
    {'nome': 'Beto', 'Idade': 23, 'cidade': 'Aracaju'},
    {'nome': 'Carla', 'Idade': 18, 'cidade': 'Alegrete'}]

df1=pd.DataFrame(dados)

# print('lista_nome :',type(lista_nome))
# print('dic_pessoa :',type(dic_pessoa))
# print('dados      :',type(dados))
# print('df         :',type(dados))
print(df1['Idade'])

#caso2
estados = ['Acre',
           'Amapá',
           'Amazonas',
           'Pará',
           'Rondônia',
           'Roraima',
           'Tocantins']

siglas=['AC','AP','AM','PA','RN','RR','TO']
df2 = pd.DataFrame(estados,columns=['estados'])

df2['siglas']=siglas
print(df2)

#caso3
capitais = [['Acre', 'AC', '803,5 mil', 'Rio Branco'],
            ['Amapá', 'AP', '776,6 mil', 'Macapá'],
            ['Amazonas', 'AM', '3,9 milhões', 'Manaus'],
            ['Pará', 'PA', '8,1 milhões', 'Belém'],
            ['Rondônia', 'RO', '1,7 milhão', 'Porto Velho'],
            ['Roraima', 'RR', '505,6 mil', 'Boa Vista'],
            ['Tocantins', 'TO', '1,5 milhão', 'Palmas']]
print(type(capitais))

print(capitais[2][2])
df3 = pd.DataFrame(capitais, columns=['Estado', 'Sigla', 'População', 'Capital'])
print(df3)

