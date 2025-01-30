import pandas as pd
import matplotlib.pylab as plt

df=pd.read_csv('clientes-v3-preparado.csv')
pd.set_option('display.width', None)

#Gráfico de Barras
plt.figure(figsize=(10,6),num='Barras')
df['nivel_educacao'].value_counts().plot(kind='bar',color='#90ee70')
plt.title('Divisao de Escolaridade')
plt.xlabel('Nivel educacao')
plt.ylabel('quantidade')
plt.xticks(rotation=0)

x=df['nivel_educacao'].value_counts().index
y=df['nivel_educacao'].value_counts().values

plt.figure(figsize=(10,6),num='barras 2')
plt.bar(x,y,color='#60aa64')
plt.title('Divisao de Escolaridade')
plt.xlabel('Nivel educacao')
plt.ylabel('quantidade')

#plt.show()
#grafico de pizza
plt.figure(figsize=(10,6),num='pizza')
plt.pie(y,labels=x,autopct='%.1f%%',startangle=90)
plt.title('distribuição do nível de educação')
plt.show()

#grafico de dispersão
plt.figure(figsize=(10,6),num='hexbin')

plt.hexbin(df['idade'],df['salario'],gridsize=40,cmap='Blues')
plt.colorbar(label='contagem dentro do bin')
plt.xlabel( 'idade')
plt.show()
