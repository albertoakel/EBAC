import pandas as pd
from sklearn.preprocessing import LabelEncoder

pd.set_option('display.width',None)
pd.set_option('display.max_colwidth',None)

df=pd.read_csv('clientes-v2-tratados.csv')

#codificacao_estado civil: 4 repostas: Solterio, casado, víuvo, divorciado
df=pd.concat([df,pd.get_dummies(df['estado_civil'],prefix='estado_civil')],axis=1)
#print(df.head())

#codificação ordinal para nível_educacional
educacao_ordem={'Ensino Fundamental':1,'Ensino Médio': 2, 'Ensino Superior':3,'Pos-graduação':4 }
df['Nivel_educacao_ordinal']=df['nivel_educacao'].map(educacao_ordem)

#codificacao area de atuacao #cat.codes
df['area_atuacao_cod']=df['area_atuacao'].astype('category').cat.codes
#listar codigos
#print(f"\n Categorias criadas pelo cat.codes: \n {df['area_atuacao'].astype('category')}")

# #label_encoder= labelEncoder()
Label_Encoder   =LabelEncoder()
df['estado_cod']=Label_Encoder.fit_transform(df['estado'])

print(df.head())
#listar codigos
#print("\nMapeamento entre os valores originais e os códigos:")
# for i, estado in enumerate(Label_Encoder.classes_):
#     print(estado, i)



