"""Funções auxiliares para avaliação e interpretação de modelos de ML.

Este módulo reúne rotinas reutilizáveis da etapa de modelagem do projeto
Diagnóstico de Hipotireoidismo. As decisões experimentais e a interpretação
 dos resultados permanecem documentadas no notebook.
"""

import pandas as pd
from sklearn.base import clone
from sklearn.inspection import permutation_importance


def importancia_permutacao_cv(
    pipeline,
    X,
    y,
    cv,
    scoring="average_precision",
    n_repeats=10,
    random_state=42,
    n_jobs=-1,
):
    """Calcula importância por permutação em cada fold da validação cruzada.

    O pipeline é ajustado somente na partição de treinamento de cada fold e
    avaliado na respectiva partição de validação. Ao final, as importâncias
    são resumidas pela média entre folds.

    Parameters
    ----------
    pipeline : estimator
        Pipeline completo de pré-processamento e classificação.
    X : pandas.DataFrame
        Preditores do conjunto de treinamento.
    y : pandas.Series ou array-like
        Variável-alvo correspondente a X.
    cv : cross-validation splitter
        Divisor utilizado para gerar os folds.
    scoring : str ou callable, default="average_precision"
        Métrica cuja redução será medida após a permutação.
    n_repeats : int, default=10
        Número de permutações por variável em cada fold.
    random_state : int, default=42
        Semente-base; cada fold utiliza uma semente distinta.
    n_jobs : int ou None, default=-1
        Número de trabalhos paralelos para permutation_importance.

    Returns
    -------
    pandas.DataFrame
        Índice por variável e colunas de importância média, variabilidade
        entre folds e desvio-padrão médio das permutações.
    """
    if not isinstance(X, pd.DataFrame):
        raise TypeError("X deve ser um pandas.DataFrame para preservar os nomes das variáveis.")
    if len(X) != len(y):
        raise ValueError("X e y devem possuir o mesmo número de observações.")

    resultados = []

    for fold, (idx_treino, idx_validacao) in enumerate(cv.split(X, y), start=1):
        X_fold_treino = X.iloc[idx_treino]
        X_fold_validacao = X.iloc[idx_validacao]
        y_fold_treino = y.iloc[idx_treino] if hasattr(y, "iloc") else y[idx_treino]
        y_fold_validacao = y.iloc[idx_validacao] if hasattr(y, "iloc") else y[idx_validacao]

        modelo_fold = clone(pipeline)
        modelo_fold.fit(X_fold_treino, y_fold_treino)

        perm = permutation_importance(
            modelo_fold,
            X_fold_validacao,
            y_fold_validacao,
            scoring=scoring,
            n_repeats=n_repeats,
            random_state=random_state + fold,
            n_jobs=n_jobs,
        )

        for i, variavel in enumerate(X.columns):
            resultados.append(
                {
                    "Fold": fold,
                    "Variavel": variavel,
                    "Importancia_media": perm.importances_mean[i],
                    "Desvio_padrao": perm.importances_std[i],
                }
            )

    df = pd.DataFrame(resultados)
    return (
        df.groupby("Variavel")
        .agg(
            Importancia_media=("Importancia_media", "mean"),
            Variabilidade_entre_folds=("Importancia_media", "std"),
            Desvio_padrao_permutacao=("Desvio_padrao", "mean"),
        )
        .sort_values("Importancia_media", ascending=False)
        .fillna(0)
    )
