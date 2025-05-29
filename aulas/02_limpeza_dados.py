import pandas as pd
#aula limpeza de dados

df=pd.read_csv('clientes.csv')
pd.set_option('display.width',None)
print(df.head())

#remover dados
df.drop('pais',axis=1,inplace=True) #coluna (axis=1)
df.drop(2,axis=0,inplace=True) # remover linha (axis=0)

##normalizar texto
df['nome']=df['nome'].str.title() #primera letra
df['endereco']=df['endereco'].str.lower() #minuculo
df['estado']=df['estado'].str.strip().str.upper()

#converter tipos de dados
df['idade']=df['idade'].astype(int)

print(df.head())

#valores nulos
#identificar valores nulos
print("valores nulos")
print(df.isnull().sum())
print('total:',df.isnull().sum().sum())

#abordagens
#df=df.fillna(0) #subtitui nulo por zero ou outro valor definido
#df=df.dropna() # remover registro nulo( Elimine as linhas onde pelo menos um elemento estiver faltando)
#df=df.dropna(thresh=4) #mantem pelo menos 4 registros não nulos
                    #ex. um dataset com 6 colunas. caso o dado tenha 2 registro nulos, ele irá remover aquela linha.
                    #assim mantem 4 linha não nulas

df=df.dropna(subset=['cpf']) #remover linha registro com cpf nulo

df.fillna({'estado':'Desconhecido'},inplace=True) #valores nulos em estado para Desconhecido
#df['estado']=df['estado'].fillna("Desconhecido") # outra forma
df.fillna({  'endereco':'End. desconhecido'},inplace=True) # Endereço nulo para end. Desconhecido
df["idade aj"]=df['idade'].fillna(df['idade'].mean()) #criar nova coluna onde atribui valor médio das idades para idades nulas

#reorganizar datas
#mudar de str-datetime
df['datetime']=pd.to_datetime(df['data'],format='%d/%m/%Y',errors="coerce")


print(df.shape)
#remove duplicadas
df.drop_duplicates(subset='cpf',inplace=True) #mesmo cpf --mesma pessoa
print(df.shape)

#trocando as colunas
df['data']  = df['datetime']
df['idade'] = df['idade aj']

df.drop('datetime',axis=1,inplace=True) #coluna (axis=1)
df.drop('idade aj',axis=1,inplace=True) #coluna (axis=1)

#salvar df
df_final=df[['nome','cpf','idade','data','endereco','estado']]
df_final.to_csv('clientes_lmpz.csv',index=False)

print('Novo DataFrame :\n',pd.read_csv('clientes_lmpz.csv'))


