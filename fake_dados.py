import pandas as pd
from faker import Faker
import random

faker=Faker('pt_BR')

dados_pessoas = []

for _ in range(100):
    nome        =   faker.name()
    cpf         =   faker.cpf()
    idade       =   random.randint(18,60)
    data        =   faker.date_of_birth(minimum_age=idade,maximum_age=idade).strftime("%d/%m/%Y")
    endereco    =   faker.address()
    estado      =   faker.address()
    pais        =   "Brasil"

    pessoa={
        'nome'      : nome,
        'cpf'       : cpf,
        'idade'     : idade,
        'data'      : data,
        'endereco'  : endereco,
        'estado'    : estado,
        'pais'      : pais
        }

    dados_pessoas.append(pessoa)

df_pessoas=pd.DataFrame(dados_pessoas)

pd.set_option('display.max_columns',None)
pd.set_option('display.max_row',None)
pd.set_option('display.max_colwidth',None)
pd.set_option('display.width',None)

print(df_pessoas)

#print(df_pessoas.to_string())
df_pessoas.to_csv('base_dados_random.csv')