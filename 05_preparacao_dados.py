import pandas as pd


df=pd.read_csv('clientes-v2.csv')

print(df.head().to_string())
print(df.tail().to_string())
df['data']=pd.to_datetime(df['data'],format='%d/%m/%Y',errors='coerce')

print('-----------------------verificação-------------------------------------------')
print(df.info())
print('dados nulos:\n', df.isnull().sum())
print('%',df.isnull().mean()*100)
df.dropna(inplace=True)
print('-----------------------verificação 2------------------------------------------')
print(df.info())
print('total nulos:', df.isnull().sum().sum())
#df.drop_duplicates(subset='cpf',inplace=True) #mesmo cpf --mesma pessoa

print('duplicados',df.duplicated().sum())
print('dados unicos:',df.nunique())

print(df.describe())

df=df[['idade','data','estado','salario','nivel_educacao','numero_filhos','estado_civil','area_atuacao']]
print(df.head().to_string())



df.to_csv('clientes-v2-tratados.csv',index=False)

print(df.info())

