import pandas as pd
from scipy import stats
#aula outlier 
pd.set_option('display.width',None)
df=pd.read_csv('clientes_lmpz.csv')
#print(df.head())

df_filtro100=df[df['idade']>100]
#print(df_filtro100)

#zscore
z_scores=stats.zscore(df['idade'])
outliers_z=df[z_scores>2/100]
#print(outliers_z)
#print('total:',outliers_z.shape[0])

df_zscore=df[(stats.zscore(df['idade'])<3)]

#IQR (Interquartile range)
li=0.25
Q1=df['idade'].quantile(li)
Q3=df['idade'].quantile(1-li)
IQR=Q3-Q1
C=1.5
limite_inferior=Q1-C*IQR
limite_superior=Q3+C*IQR

#print('limites IQR',limite_inferior,limite_superior)
outliers_iqr=df[(df['idade']< limite_inferior) | (df['idade']> limite_superior)]
#print('valores outliers_iqr',outliers_iqr)
#print('total',outliers_iqr.shape[0])
df_iqr=df[(df['idade']< limite_inferior) & (df['idade']> limite_superior)]


limite_inferior=1
limite_superior=100
df_iqr=df[(df['idade']< limite_inferior) & (df['idade']> limite_superior)]

# filtra endereço invalido
df['endereco']=df['endereco'].apply(lambda x: 'Endereco inválido' if len(x.split('\n'))<3 else x)
print('total endereco grandes',(df['endereco']=='Endereco inválido').sum())

# filtra nomes grandes
df['nome']=df['nome'].apply(lambda x: 'Nome inválido' if isinstance(x,str) and len(x) > 50 else x)

print('total Nomes grandes',(df['nome']=='Nome inválido').sum())

df.to_csv('clientes_rmv_outliers.csv',index=False)
print('Novo DataFrame :\n',pd.read_csv('clientes_rmv_outliers.csv'))


