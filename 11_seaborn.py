import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns

df=pd.read_csv('clientes-v3-preparado.csv')
pd.set_option('display.width', None)


# Gráfico de Dispersão
plt.figure(num=1)
sns.jointplot(x='idade', y='salario', data=df, kind='scatter') # ['scatter', 'hist', 'hex', 'kde', 'reg', 'resid']


# Gráfico de Densidade
plt.figure(figsize=(10, 6))
sns.kdeplot(df['salario'], fill=True, color='#863e9c')
plt.title('Densidade de slários')
plt.xlabel('Salário')
# plt.show()

# Gráfico de Pairplt - Dispersão e Histograma
plt.figure(figsize=(10, 6))
sns.pairplot(df[['idade', 'salario', 'anos_experiencia', 'nivel_educacao']])
# plt.show()

# Gráfico de Regressão
plt.figure(figsize=(10, 6))
sns.regplot(x='idade', y='salario', data=df, color='#278f65', scatter_kws={'alpha': 0.5, 'color': '#34c289'})
plt.title('Regressão de salário por Idade')
plt.xlabel('Idade')
plt.ylabel('Salário')
# plt.show()

# Gráfico countplot com hue
plt.figure(figsize=(10, 6))
sns.countplot(x='estado_civil', hue='nivel_educacao', data=df, palette='pastel')
plt.xlabel('Estado Civil')
plt.ylabel('Quantidade Clientes')
plt.legend(title='Nivel de Educação')
plt.show()
