import numpy as np
from scipy import stats
from scipy.stats import norm

def teste_hipotese(amostra, valor_referencia, desvio_padrao_populacional=None, hipotese_alternativa='diferente'):
    """
    Realiza um teste de hipótese (Z-test ou t-test) com base na hipótese alternativa fornecida.

    Parâmetros:
        amostra (array-like): A amostra de dados.
        valor_referencia (float): O valor de referência para a hipótese nula (H0).
        desvio_padrao_populacional (float, opcional): O desvio padrão populacional (σ). Se não for fornecido, será usado o t-test.
        hipotese_alternativa (str): A hipótese alternativa. Pode ser 'maior', 'menor' ou 'diferente'.

    Retorna:
        None (os resultados são impressos diretamente).
    """
    # Tamanho da amostra
    n = len(amostra)

    # Média da amostra
    media_amostra = np.mean(amostra)

    # Verificar se o teste é Z ou t
    if desvio_padrao_populacional is not None:
        # Teste Z
        print("Usando o teste Z (desvio padrão populacional conhecido).")
        estatistica = (media_amostra - valor_referencia) / (desvio_padrao_populacional / np.sqrt(n))
        distribuicao = norm  # distribuicao normal padrão
    else:
        # Teste t
        print("Usando o teste t (desvio padrão populacional desconhecido).")
        desvio_padrao_amostra = np.std(amostra, ddof=1)  # Desvio padrão amostral
        estatistica = (media_amostra - valor_referencia) / (desvio_padrao_amostra / np.sqrt(n))
        distribuicao = stats.t(df=n-1)  # distribuicao t de Student

    # Calcular o valor-p com base na hipótese alternativa
    if hipotese_alternativa == 'maior':
        p_value = 1 - distribuicao.cdf(estatistica)  # Teste unicaudal à direita
        tipo_teste = "unicaudal à direita"
    elif hipotese_alternativa == 'menor':
        p_value = distribuicao.cdf(estatistica)  # Teste unicaudal à esquerda
        tipo_teste = "unicaudal à esquerda"
    elif hipotese_alternativa == 'diferente':
        p_value = 2 * (1 - distribuicao.cdf(abs(estatistica)))  # Teste bicaudal
        tipo_teste = "bicaudal"
    else:
        raise ValueError("Hipótese alternativa inválida. Use 'maior', 'menor' ou 'diferente'.")

    # Exibir os resultados
    print(f"\nMédia da amostra: {media_amostra:.2f}")
    print(f"Estatística do teste: {estatistica:.2f}")
    print(f"Valor-p ({tipo_teste}): {p_value:.4f}")

    # Interpretação
    alpha = 0.05  # Nível de significância
    if p_value < alpha:
        print(f"Rejeitamos a hipótese nula (H0). A média da amostra é significativamente {hipotese_alternativa} que {valor_referencia}.")
    else:
        print(f"Não rejeitamos a hipótese nula (H0). Não há evidências de que a média da amostra seja {hipotese_alternativa} que {valor_referencia}.")


# Exemplo de uso
np.random.seed(42)  # Para reproducibilidade
notas = np.random.normal(7.0, 1.0, size=1000)  # 1000 notas com média 7.2 e desvio padrão 1

# # Teste 1: Verificar se a média é maior que 7.0 (unicaudal à direita)
# print("\nTeste 1: Média maior que 7.0")
# teste_hipotese(notas, valor_referencia=7.0, desvio_padrao_populacional=1.0, hipotese_alternativa='maior')

# # Teste 2: Verificar se a média é menor que 7.0 (unicaudal à esquerda)
# print("\nTeste 2: Média menor que 7.0")
# teste_hipotese(notas, valor_referencia=7.0, desvio_padrao_populacional=1.0, hipotese_alternativa='menor')

# Teste 3: Verificar se a média é diferente de 7.0 (bicaudal)
print("\nTeste 3: Média diferente de 7.0")
teste_hipotese(notas, valor_referencia=7.0, desvio_padrao_populacional=1.0, hipotese_alternativa='diferente')


import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t

# Parâmetros
df = 9  # Graus de liberdade
alpha = 0.05  # Nível de significância
t_obs = -0.189  # Estatística de teste observada

# Calcular o p-valor
if t_obs < 0:
    p_value = 2 * t.cdf(t_obs, df)
else:
    p_value = 2 * (1 - t.cdf(t_obs, df))

# Gerar valores para o eixo x
x = np.linspace(-4, 4, 1000)
y = t.pdf(x, df)  # Densidade de probabilidade da distribuicao t de Student

# Criar o gráfico
plt.figure(figsize=(10, 6))
plt.plot(x, y, label=f"distribuicao t de Student  (df = {df})")

# Preencher as áreas de rejeição (caudas)
critical_value = t.ppf(1 - alpha/2, df)  # Valor crítico positivo
plt.fill_between(x, y, where=(x <= -critical_value), color='red', alpha=0.5, label=f"Área de rejeição (α/2 = {alpha/2:.3f})")
plt.fill_between(x, y, where=(x >= critical_value), color='red', alpha=0.5)

# Adicionar linha para a estatística de teste observada
plt.axvline(t_obs, color='blue', linestyle='--', label=f"t observado = {t_obs:.3f}")

# Adicionar título e legendas
plt.title(f"Teste Bicaudal com α = {alpha}\np-valor = {p_value:.3f}")
plt.xlabel("Valor t")
plt.ylabel("Densidade de probabilidade")
plt.legend()
plt.grid()
plt.show()
