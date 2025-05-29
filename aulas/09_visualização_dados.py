import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns

df=pd.read_csv('clientes-v3-preparado.csv')
pd.set_option('display.width', None)

#print(df.head())
plt.figure(num='salario')
plt.hist(df['salario'])


plt.figure(figsize=(10,6),num='Histograma salario')
plt.hist(df['salario'],bins=100,color='green',alpha=0.8)
plt.title('Histograma - distribuição salário')
plt.xlabel('Salário')
#range(0,max_salario+2000,2000)
plt.xticks(ticks=range( 0,int( df['salario'].max() ) +2000,2000))
plt.ylabel('Frequencia')
plt.grid(True)


#multiplos graficos
plt.figure(figsize=(10,6),num=3)
plt.subplot(2,2,1) #2x2 posição 1

plt.scatter(df['salario'],df['salario'])
plt.title('Dispersao - salario X salario')
plt.xlabel('salario')
plt.ylabel('salario')

plt.subplot(1,2,2) #1x2 posição 2
plt.scatter(df['salario'],df['anos_experiencia'],color='#5BB3aB',alpha=0.6,s=30)
plt.title('Dispersao - salario x anos de experiencia')
plt.xlabel('salario')
plt.ylabel('Anos de Experiencia')

corr=df[['salario','anos_experiencia']].corr()
plt.subplot(2,2,3) #2x2 posição 3
sns.heatmap(corr,annot=True,cmap='coolwarm')
plt.title('Correlaçao salariossss idade')
plt.tight_layout()
plt.show()