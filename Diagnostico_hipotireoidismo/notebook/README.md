# Notebooks --- Diagnóstico de Hipotireoidismo

Esta pasta reúne os notebooks utilizados no desenvolvimento do projeto.
Os arquivos estão organizados em duas etapas analíticas  **análise
exploratória e preparação dos dados** e **modelagem preditiva** 

## Visão geral

  ------------------------------------------------------------------------
  Notebook                 Finalidade              Quando executar
  ------------------------ ----------------------- -----------------------
  `01_EDA.ipynb`           Análise exploratória,   Primeiro
                           avaliação da qualidade  
                           dos dados, preparação   
                           da base e criação dos   
                           conjuntos de            
                           treinamento e validação 

  `02_ML.ipynb`            Pré-processamento,      Após a EDA
                           comparação dos modelos, 
                           validação cruzada,      
                           interpretação e         
                           avaliação final         


------------------------------------------------------------------------
------------------------------------------------------------------------

## 1. `01_EDA.ipynb` --- Análise Exploratória dos Dados

**Objetivo:** conhecer a estrutura da base `Hypothyroid.csv`, avaliar a
qualidade dos dados e preparar os conjuntos utilizados na etapa de
Machine Learning.

### Etapas desenvolvidas

1.  Configuração do ambiente e carregamento da base.
2.  Inspeção inicial e identificação dos tipos de variáveis.
3.  Auditoria da qualidade e consistência dos dados.
4.  Identificação de registros duplicados e verificação de valores
    inválidos na variável idade.
5.  Análise da distribuição da variável-alvo.
6.  Análise das variáveis numéricas:
    -   distribuições e valores extremos;
    -   estatísticas descritivas por classe;
    -   comparação de medianas e quartis;
    -   correlação entre variáveis;
    -   assimetria e valores ausentes.
7.  Análise das variáveis categóricas e clínicas.
8.  Síntese dos problemas identificados e das decisões de preparação.
9.  Preparação da base analítica e divisão estratificada dos dados.
10. Exportação dos conjuntos para utilização no notebook de ML.

### Principais saídas

-   Base analítica preparada.
-   `data/df_treino.csv`.
-   `data/df_validacao.csv`.
-   Estatísticas, tabelas e visualizações utilizadas para caracterizar
    os dados.

**Dependência:** arquivo `data/Hypothyroid.csv`.

**Importante:** execute este notebook antes do `02_ML.ipynb`, pois ele
prepara e exporta os arquivos utilizados na modelagem.

------------------------------------------------------------------------

## 2. `02_ML.ipynb` --- Modelagem Preditiva

**Objetivo:** comparar algoritmos de classificação para reproduzir os
rótulos da variável `binaryClass`, interpretar a contribuição dos
atributos e avaliar os modelos finalistas.

### Etapas desenvolvidas

1.  Configuração do ambiente e carregamento dos dados de treinamento.
2.  Auditoria do conjunto de treinamento e da variável-alvo.
3.  Identificação dos tipos de variáveis e remoção de atributos
    constantes.
4.  Construção do pipeline de pré-processamento:
    -   imputação e padronização de variáveis numéricas;
    -   imputação e codificação de variáveis binárias;
    -   imputação e One-Hot Encoding de variáveis categóricas.
5.  Comparação dos modelos:
    -   Dummy Classifier;
    -   Regressão Logística;
    -   Random Forest;
    -   XGBoost.
6.  Avaliação por validação cruzada estratificada em cinco folds.
7.  Análise da estabilidade dos modelos entre os folds.
8.  Importância das variáveis por permutação.
9.  Análise de sensibilidade com retirada da variável `TSH`.
10. Importância dos atributos no cenário sem TSH.
11. Associação entre variáveis categóricas e a classe, utilizando V de
    Cramer e testes estatísticos.
12. Síntese dos experimentos e seleção dos modelos finalistas.
13. Avaliação final dos modelos no conjunto de validação reservado.
14. Conclusões dos experimentos.

### Modelos e métricas

Os modelos são comparados por:

-   Precision;
-   Recall;
-   F1;
-   PR-AUC;
-   ROC-AUC.

A classe `N` é tratada como classe positiva (`1`) nas métricas de
classificação.

### Principais saídas

-   Resultados da validação cruzada.
-   Comparação dos modelos e seleção dos finalistas.
-   Importâncias por permutação.
-   Resultados do experimento sem TSH.
-   Matrizes de confusão e métricas na validação reservada.

**Dependências:** `data/df_treino.csv`, `data/df_validacao.csv` e
funções auxiliares de `src/ml_utils.py`, além dos módulos utilizados no
pré-processamento e nos modelos.

**Importante:** o conjunto de validação reservado é utilizado somente na
etapa final. Ele não deve orientar a seleção ou o ajuste dos modelos
durante o desenvolvimento.

------------------------------------------------------------------------


## Ordem recomendada de execução

Para reproduzir o fluxo analítico completo:

``` text
01_EDA.ipynb
      |
      v
02_ML.ipynb
```


## Dependências e ambiente

Os notebooks foram desenvolvidos em Python e utilizam bibliotecas para
manipulação de dados, visualização, estatística e aprendizado de
máquina, incluindo:

-   NumPy;
-   Pandas;
-   Matplotlib;
-   Seaborn;
-   SciPy;
-   Scikit-learn;
-   XGBoost;
-   Jupyter Notebook.

As funções auxiliares do projeto estão na pasta `src/`, especialmente em
`utils.py` e `ml_utils.py`.

Antes de executar, verifique se o ambiente Python possui as dependências
instaladas e se os arquivos de dados estão nos caminhos esperados.

## Relação com o relatório

O relatório geral está em `docs/relatorio_geral.md`. As imagens
referenciadas no documento ficam em `docs/figuras/`.

Os notebooks principais documentam os procedimentos e resultados
analíticos. Os notebooks auxiliares permitem regenerar as figuras
utilizadas na apresentação dos resultados.
