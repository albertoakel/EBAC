import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
plt.close('all')



# 1-Gráfico de Histograma
#
# 2-Gráfico de dispersão
#
# 3-Mapa de calor
#
# 4-Gráfico de barra
#
# 5-Gráfico de pizza
#
# 6-Gráfico de densidade
#
# 7-Gráfico de Regressão


df=pd.read_csv('ecommerce_preparados.csv')
#print(df.keys())
#print(df.shape)
pd.set_option('display.max_columns',None)
pd.set_option('display.max_row',50)
#pd.set_option('display.max_colwidth',None)
pd.set_option('display.width',None)


df.sort_values("Título", ascending=True)

#remover colunas review
df.drop(columns=['Review1', 'Review2', 'Review3'],inplace=True)

#Considerar NaN como sem desconto, logo NaN-> zero
df['Desconto']=df['Desconto'].fillna(0)
#print(df[['Título', 'Nota']])
print('total=',len(df['Título']))
#print(df.isnull().sum().sum())
df_title = df.groupby('Título').sum()
print('total=',df_title.shape)

print(df_title)

# print(df['Título'].nunique())
# print(df.shape)
# print(df['Marca'].nunique())

#print(f"\n Categorias criadas pelo cat.codes: \n {df['Marca'].astype('category')}")


#1) HISTOGRAMA
#plt.hist(df['Preço'],bins=100,color='green',alpha=0.8)
#plt.title('Histograma - distribuição salário')
#plt.xlabel('Salário')
#range(0,max_salario+2000,2000)
#plt.xticks(ticks=range( 0,int( df['salario'].max() ) +2000,2000))
#plt.ylabel('Frequencia')
#plt.grid(True)
# plt.figure(figsize=(10,6),num='Histograma salario')
# plt.hist(df['Marca_Cod'],bins=100,color='green',alpha=0.8)
# plt.title('Histograma - distribuição salário')
# plt.xlabel('Salário')
# #range(0,max_salario+2000,2000)
# #plt.xticks(ticks=range( 0,int( df['salario'].max() ) +2000,2000))
# plt.ylabel('Frequencia')
# plt.grid(True)
#plt.show()

# #1) GRAFICO DISPERSÃO
#
# plt.figure(figsize=(10,6),num='dispersao 1')
# plt.scatter(df['Nota'],df['N_Avaliações'],color='#5BB3aB',alpha=0.75,s=30)
# plt.title('Nota X Preço ')
# plt.xlabel('Nota')
# plt.ylabel('Preço')
#
# #plt.figure(figsize=(10,6),num='mosaico')
# #sns.pairplot(df[['Preço', 'Desconto' ,'Nota']])
#
#sns.jointplot(x='N_Avaliações', y='Nota', data=df, kind='scatter') # ['scatter', 'hist', 'hex', 'kde', 'reg', 'resid']
#
#
# #1 GRAFICO DE BARRA
#
# x=df['Nota'].value_counts().index
# y=df['Nota'].value_counts().values
#
# plt.figure(figsize=(10,6),num='barras 2')
# plt.bar(x,y,color='#60aa64')
# plt.title('Nota')
# plt.xlabel('NOTA')
# plt.ylabel('quantidade')
#
#
# #1 grafico de densidade
# plt.figure(figsize=(10,6),num='Densidade')
# sns.kdeplot(df['Nota'], fill=True, color='#670105')
# plt.title('Densidade dos Notas')
# plt.xlabel('Nota')
#
# plt.figure(figsize=(10,6),num='Densidade')
# sns.kdeplot(df['Nota'], fill=True, color='#670105')
# plt.title('Densidade dos preços')
# plt.xlabel('Preços')
# ##1 Mapa de calor
# #corr=df[['Preço','Desconto']].corr()
# #sns.heatmap(corr,annot=True,cmap='coolwarm')
# #plt.title('preçoX Desconto')
# #plt.tight_layout()
# plt.show()

from matplotlib.colors import LinearSegmentedColormap

# Criando um colormap personalizado (Teal → Branco → Orange)
teal_orange = LinearSegmentedColormap.from_list("TealOrange", ["#008080", "#FFFFFF", "#FF7700"])

# Criando o heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(df, cmap=teal_orange, annot=True, linewidths=0.5)

plt.title("Heatmap com Teal & Orange (Custom)")
plt.show()