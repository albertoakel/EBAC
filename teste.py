import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Definir os números de bits que você deseja plotar
bits_a_plotar = [1, 2, 4, 8]

# Lista para armazenar os dados de todos os pontos
dados_para_grafico = []

# Um limite seguro para num_estados antes de estourar int64 (2^63 - 1 é o máximo)
MAX_INT64_SAFE_FOR_RANDINT = 2 ** 60  # Usando um valor conservador para evitar estouro em np.random.randint

# Número de amostras para N grandes (para a computação quântica)
# Ajuste este valor para controlar a densidade de pontos para N grande
NUM_AMOSTRAS_PARA_N_GRANDE = 200

for n in bits_a_plotar:
    num_estados = 2 ** n  # Número total de estados para 'n' bits

    # --- Dados para Computação Clássica ---
    # Para num_estados muito grandes, não podemos usar np.random.randint diretamente para o intervalo completo.
    # Em vez disso, vamos escolher um valor aleatório dentro de um intervalo seguro para representar o ponto.
    if num_estados > MAX_INT64_SAFE_FOR_RANDINT:
        # Para fins de visualização, basta um ponto representativo para N alto.
        # Escolhemos um valor aleatório pequeno para que ele seja visível na parte inferior do gráfico log.
        resposta_classica_aleatoria = np.random.randint(0, 100)
    else:
        # Para num_estados dentro do limite do int64, podemos usar o intervalo completo
        resposta_classica_aleatoria = np.random.randint(0, num_estados)

    dados_para_grafico.append({
        'Numero_de_Bits': n,
        'Resposta_Decimal': resposta_classica_aleatoria,
        'Tipo_Computacao': 'Clássica'
    })

    # --- Dados para Computação Quântica ---
    # Para N pequeno (<= 16), plotamos TODOS os estados.
    if n <= 16:
        for estado_decimal in range(num_estados):
            dados_para_grafico.append({
                'Numero_de_Bits': n,
                'Resposta_Decimal': estado_decimal,
                'Tipo_Computacao': 'Quântica'
            })
    # Para N grande (> 16), onde plotar todos os 2^N estados é inviável,
    # plotamos uma AMOSTRA representativa.
    else:
        # Gerar amostras aleatórias dentro do intervalo [0, num_estados - 1]
        # Usamos np.random.uniform para gerar números float no intervalo e depois convertemos para int.
        # Isso evita o problema de np.random.randint com 'high' muito grande.
        amostras_quanticas = np.random.uniform(0, num_estados, NUM_AMOSTRAS_PARA_N_GRANDE).astype(int)

        # Garante que 0 e num_estados-1 também sejam incluídos para mostrar o intervalo completo
        amostras_quanticas = np.unique(np.concatenate(([0, num_estados - 1], amostras_quanticas)))

        for estado_decimal in amostras_quanticas:
            dados_para_grafico.append({
                'Numero_de_Bits': n,
                'Resposta_Decimal': estado_decimal,
                'Tipo_Computacao': 'Quântica'
            })

# Criar DataFrame para Seaborn
df = pd.DataFrame(dados_para_grafico)

# --- Ajuste do Tamanho dos Pontos ---
# O Seaborn tem problemas para lidar com valores de 'size' extremamente grandes.
# Se 'Resposta_Decimal' para N=128 for usada diretamente, seria enorme.
# Precisamos escalar 'Resposta_Decimal' para o 'size' dos pontos.
# Vamos usar o log da Resposta_Decimal para o tamanho, mas com um limite.
df['Tamanho_Ponto'] = np.log1p(df['Resposta_Decimal'])  # log1p é log(1 + x) para lidar com 0

# Ajuste para garantir que pontos de N grande tenham um tamanho visível e comparável
# Mesmo com log1p, valores para N=128 serão muito maiores que N=16.
# Vamos normalizar o Tamanho_Ponto para que os pontos maiores não dominem completamente.
max_log_size_n_16 = np.log1p(2 ** 16 - 1)  # Tamanho log máximo para N=16
df.loc[df['Numero_de_Bits'] > 16, 'Tamanho_Ponto'] = df.loc[df['Numero_de_Bits'] > 16, 'Tamanho_Ponto'].clip(
    upper=max_log_size_n_16 * 1.5)

# 2. Criar o gráfico de dispersão com Seaborn
plt.figure(figsize=(14, 8))  # Aumentar o tamanho da figura para melhor visualização de muitos pontos

sns.scatterplot(
    data=df,
    x='Numero_de_Bits',
    y='Resposta_Decimal',
    hue='Tipo_Computacao',
    size='Tamanho_Ponto',  # Usamos a coluna 'Tamanho_Ponto' para controlar o tamanho
    sizes=(20, 1000),  # Ajuste a faixa de tamanho para melhor visualização.
    palette={'Quântica': 'blue', 'Clássica': 'red'},
    alpha=0.6,  # Transparência para ver sobreposição de pontos
    legend='full'
)

# 3. Personalizar o gráfico
plt.title('Representação dos Estados: Clássica vs. Quântica por Número de Bits (N)', fontsize=16)
plt.xlabel('Número de Bits (N)', fontsize=14)
plt.ylabel('Resposta dos Estados (Valor Decimal)', fontsize=14)
plt.yscale('log')  # Usar escala logarítmica no eixo Y é CRÍTICO para N alto, devido à grande variação de 2^N
plt.grid(True, which="both", ls="--", c='0.7')  # Adicionar grade para ambos os eixos
plt.xticks(bits_a_plotar)  # Garante que todos os Ns sejam mostrados no eixo X
plt.tight_layout()  # Ajusta o layout para evitar sobreposição
plt.show()