import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt

# testes adicionais
from scipy.stats import cramervonmises

from scipy.stats import (norm, expon, lognorm, gamma, beta, weibull_min,
                         gumbel_r, triang, uniform, anderson, kstest)


def identify_distribution(data, dist_names=None, plot=True, alpha=0.05):
    """
    Identifica a melhor distribuição que se ajusta aos dados.

    Parâmetros:
    -----------
    data : pd.Series ou np.array
        Dados a serem analisados.
    dist_names : list, opcional
        Lista de distribuições a testar. Padrão: ['norm', 'expon', 'lognorm', 'gamma', 'beta'].
    plot : bool, opcional
        Se True, plota o histograma com as curvas ajustadas.
    alpha : float, opcional
        Nível de significância para testes de hipótese (padrão: 0.05).

    Retorna:
    --------
    dict
        Dicionário com as distribuições testadas, estatísticas de ajuste e o melhor ajuste.
    """
    if dist_names is None:
        # dist_names = ['norm', 'expon', 'lognorm', 'gamma', 'weibull_min', 'gumbel_r']

        dist_names = [
    'norm', 'expon', 'lognorm', 'gamma', 'weibull_min', 'gumbel_r',
    'beta', 'triang', 'uniform', 'logistic', 'rayleigh', 'pareto']

    results = {}
    best_fit = None
    best_stat = np.inf  # Quanto menor, melhor (para KS e Anderson-Darling)

    # Loop sobre as distribuições
    for dist_name in dist_names:
        try:
            # Ajuste da distribuição
            dist = getattr(stats, dist_name)
            params = dist.fit(data)

            # Teste de Kolmogorov-Smirnov
            ks_stat, ks_pval = kstest(data, dist_name, args=params)

            # Teste de Anderson-Darling (se disponível)
            anderson_stat = None
            if dist_name in ['norm', 'expon', 'gumbel_r', 'logistic']:
                anderson_result = anderson(data, dist_name)
                anderson_stat = anderson_result.statistic

            # Teste de Cramér-von Mises (diferenca quadratica CDFS)
            cvm_result = cramervonmises(data,dist_name, args=params)
            # Armazena resultados
            results[dist_name] = {
                'params': params,
                'ks_stat': ks_stat,
                'ks_pval': ks_pval,
                'anderson_stat': anderson_stat,
                'cvm_stat': cvm_result.statistic
            }
            # Atualiza melhor ajuste (menor estatística KS ou Anderson)
            if anderson_stat is not None:
                if anderson_stat < best_stat:
                    best_stat = anderson_stat
                    best_fit = dist_name
            else:
                if ks_stat < best_stat:
                    best_stat = ks_stat
                    best_fit = dist_name

        except Exception as e:
            print(f"Erro ao ajustar {dist_name}: {e}")
            continue

    # Plotagem (opcional)
    if plot:
        plt.figure(figsize=(10, 6))
        plt.hist(data, bins='auto', density=True, alpha=0.6, color='g', label='Dados')

        x = np.linspace(min(data), max(data), 1000)
        for dist_name, result in results.items():
            dist = getattr(stats, dist_name)
            pdf = dist.pdf(x, *result['params'])
            plt.plot(x, pdf, label=f"{dist_name} (KS={result['ks_stat']:.3f})")

        plt.legend()
        plt.title("Ajuste de Distribuições")
        plt.show()

    data = []
    for dist_name, metrics in results.items():
        row = {
            'Distribution': dist_name,
            'Params': metrics['params'],
            'KS_Stat': metrics['ks_stat'],
            'KS_p-value': metrics['ks_pval'],
            'Anderson_Stat': metrics['anderson_stat'],
            'cvm_stat': metrics['cvm_stat'],
            'Is_Best_Fit': (dist_name == best_fit)}
        data.append(row)

    # Criar DataFrame
    df = pd.DataFrame(data)


    return best_fit,df
