import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Exemplo de DataFrame
data = {'idade': [25, 45, 35, 50],
        'salário': [50000, 100000, 75000, 120000]}
df = pd.DataFrame(data)

# Padronização
scaler = StandardScaler()
df['idade_padronizada'] = scaler.fit_transform(df[['idade']])
df['salário_padronizado'] = scaler.fit_transform(df[['salário']])

# Normalização
min_max_scaler = MinMaxScaler()
df['idade_normalizada'] = min_max_scaler.fit_transform(df[['idade']])
df['salário_normalizado'] = min_max_scaler.fit_transform(df[['salário']])

print(df)