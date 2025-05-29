import pandas as pd

df=pd.read_csv('clientes.csv')

#verificar registros
print(df.head().to_string)
print(df.tail().to_string)

print('Qtd:',df.shape)
print('Tipagem:\n',df.dtypes)
print('valores nulos:\n',df.isnull().sum)


#expressão lambda( abordagem simples com uso de apply em dataframe)
#ex1:
eleva_cubo_lambda= lambda x: x**3
#print(eleva_cubo_lambda(3))
A=[1,2,3,4,5]
#print( A.apply(lambda x: x**3) )

#print(eleva_cubo_lambda(A))
