import pandas as pd
import numpy as np
from scipy import stats

pd.set_option('display.width', None)

df=pd.read_csv('clientes-v2-tratados.csv')
#print(df.head())

#escala log
df['salario_log']=np.log1p(df['salario']) #evitar saltos núméricos
#print(df.head())
#Transformacao Box-cox
df['salario_boxcox'], _ = stats.boxcox(df['salario']+1)

#codificacao de frequencia para 'estado'
estado_freq = df['estado'].value_counts()/len(df)
df['estado_freq']=df['estado'].map(estado_freq)

#interação. relacao idadexfilhos
df['interacao_idade_filhos']= df['idade']*['numero_filhos']

print(df.head())
