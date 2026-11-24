# Diagnóstico de Hipotireoidismo

Projeto desenvolvido como parte da formação em **Ciência de Dados da
EBAC**, com foco em análise exploratória de dados e modelagem de
classificação binária aplicada à base `Hypothyroid.csv`.

O trabalho investiga os dados disponíveis, realiza a preparação para
modelagem, compara algoritmos de Machine Learning e avalia a capacidade
dos modelos de reproduzir a variável-alvo `binaryClass`.

> **Nota de escopo:** os modelos foram desenvolvidos para reproduzir os
> rótulos presentes na base. Os resultados não constituem validação
> clínica de diagnóstico de hipotireoidismo e não substituem avaliação
> profissional.

## Objetivos

-   Caracterizar a base e investigar a distribuição das variáveis.
-   Identificar valores ausentes, duplicidades, valores inválidos e
    atributos sem variabilidade.
-   Analisar diferenças entre as classes e relações entre os atributos.
-   Preparar os dados com separação entre treinamento e validação
    reservada.
-   Comparar modelos de classificação por validação cruzada
    estratificada.
-   Investigar a importância dos atributos e a sensibilidade dos modelos
    à retirada de TSH.
-   Avaliar os modelos finalistas em dados não utilizados durante o
    desenvolvimento.

## Base de dados

A base utilizada é `Hypothyroid.csv`, originalmente composta por **3.772
registros e 30 colunas**.

Os atributos incluem informações demográficas, histórico de tratamentos
e procedimentos relacionados à tireoide, indicadores de realização de
exames, resultados laboratoriais e a variável-alvo `binaryClass`.

### Variável-alvo

A variável `binaryClass` possui duas categorias:

  -------------------------------------------------------------------------
  Rótulo                   Codificação Interpretação    Registros originais
                                       na modelagem    
  --------------- -------------------- --------------- --------------------
  `P`                                0 Classe negativa       3.481 (92,29%)

  `N`                                1 Classe positiva          291 (7,71%)
  -------------------------------------------------------------------------

A classe `N` foi definida como positiva para o cálculo das métricas de
Precision, Recall, F1 e PR-AUC. A interpretação clínica dos rótulos
depende da documentação de sua construção.

## Etapas do projeto

### 1. Análise exploratória e preparação dos dados

A análise exploratória investigou:

-   distribuição das variáveis numéricas e categóricas;
-   distribuição da variável-alvo;
-   valores ausentes e assimetria;
-   duplicidades e valores inválidos;
-   diferenças entre as classes;
-   correlação entre variáveis numéricas;
-   associação entre variáveis categóricas e a classe.

Na preparação, foram removidas as 61 duplicatas excedentes, o valor
inválido de idade foi convertido em ausente, e as variáveis `TBG` e
`TBG measured` foram excluídas. Após esses procedimentos, a base
analítica ficou com **3.711 registros**.

A divisão estratificada, com 80% para treinamento e 20% para validação
reservada (`random_state=42`), resultou em:

  Conjunto                Registros
  --------------------- -----------
  Treinamento                 2.968
  Validação reservada           743
  **Total**               **3.711**

A validação reservada foi mantida separada durante o desenvolvimento,
sendo utilizada somente na avaliação final dos modelos selecionados.

### 2. Modelagem

Foram comparados quatro classificadores:

-   Dummy Classifier;
-   Regressão Logística;
-   Random Forest;
-   XGBoost.

O pré-processamento foi integrado aos pipelines, com imputação de
valores ausentes e transformações específicas para variáveis numéricas,
binárias e categóricas.

A comparação foi realizada com **validação cruzada estratificada de
cinco folds**, utilizando `shuffle=True` e `random_state=42`.

As métricas adotadas foram:

-   Precision;
-   Recall;
-   F1;
-   PR-AUC;
-   ROC-AUC.

### 3. Interpretação e avaliação

Após a comparação, XGBoost e Random Forest foram selecionados como
modelos finalistas. Também foram realizadas análises de importância por
permutação, um experimento de sensibilidade sem a variável TSH e testes
de associação entre variáveis categóricas e a classe.

Os modelos finalistas foram ajustados com todo o conjunto de treinamento
e avaliados nos 743 registros reservados.

## Principais resultados

### Validação cruzada

  Modelo                  Precision   Recall      F1   PR-AUC   ROC-AUC
  --------------------- ----------- -------- ------- -------- ---------
  Dummy                       0,000    0,000   0,000    0,079     0,500
  Regressão Logística         0,723    0,940   0,817    0,875     0,989
  Random Forest               0,926    0,991   0,957    0,990     0,999
  XGBoost                     0,958    0,974   0,966    0,976     0,996

### Avaliação na validação reservada

  Modelo            Precision   Recall      F1   PR-AUC   ROC-AUC
  --------------- ----------- -------- ------- -------- ---------
  XGBoost               1,000    0,983   0,991    1,000     1,000
  Random Forest         0,983    1,000   0,992    1,000     1,000

Cada modelo finalista apresentou apenas um erro de classificação na
validação reservada: o XGBoost registrou um falso negativo, enquanto o
Random Forest registrou um falso positivo.

### Achados da interpretação

-   TSH apresentou a maior importância por permutação nos modelos
    avaliados.
-   A retirada de TSH provocou redução expressiva do desempenho dos três
    modelos.
-   Sem TSH, TT4, FTI e T3 passaram a concentrar maior importância
    relativa.
-   `on thyroxine` e `query hypothyroid` apresentaram associação
    estatística com a classe, mas com baixa intensidade segundo o V de
    Cramer.

## Limitações e cuidados de interpretação

-   A origem e o procedimento de construção de `binaryClass` não foram
    estabelecidos de forma independente. Caso TSH tenha participado da
    definição dos rótulos, pode existir circularidade ou vazamento de
    informação; os resultados disponíveis não permitem confirmar essa
    hipótese.
-   A validação reservada pertence à mesma base de origem do
    treinamento. Não foi realizada validação externa em outra população
    ou instituição.
-   A classe positiva possui 233 registros no treinamento e 58 na
    validação reservada, o que limita a precisão das estimativas.
-   A importância por permutação representa contribuição preditiva no
    contexto dos modelos, não causalidade.
-   O desempenho observado demonstra capacidade de reproduzir os rótulos
    do conjunto avaliado; não comprova eficácia diagnóstica ou
    generalização clínica.

## Estrutura do projeto

``` text
Diagnostico_hipotireoidismo/
├── data/
│   ├── Hypothyroid.csv
│   ├── df_treino.csv
│   └── df_validacao.csv
├── notebook/
│   ├── 01_EDA.ipynb
│   ├── 02_ML.ipynb
│   ├── 01_EDA_figuras.ipynb
│   └── 02_ML_figuras.ipynb
├── src/
│   ├── utils.py
│   └── ml_utils.py
└── docs/
    ├── relatorio_geral.md
    └── figuras/
        ├── eda_01.png
        ├── ...
        ├── eda_12.png
        ├── ml_01.png
        ├── ...
        └── ml_08.png
```

A estrutura acima representa a organização prevista para a entrega. Os
arquivos de dados devem estar disponíveis localmente para executar os
notebooks.

## Como executar

### 1. Clonar o repositório

``` bash
git clone <URL_DO_REPOSITORIO>
cd Diagnostico_hipotireoidismo
```

### 2. Criar e ativar um ambiente Python

Exemplo utilizando Conda:

``` bash
conda create -n hipotireoidismo python=3.11
conda activate hipotireoidismo
```

### 3. Instalar as dependências

As bibliotecas utilizadas incluem:

``` bash
pip install numpy pandas matplotlib seaborn scipy scikit-learn xgboost jupyter ipykernel
```

### 4. Disponibilizar os dados

Mantenha `Hypothyroid.csv` no diretório `data/`. Os arquivos
`df_treino.csv` e `df_validacao.csv` são utilizados pelo notebook de
modelagem, conforme a etapa de preparação documentada no projeto.

### 5. Executar os notebooks

Abra o Jupyter:

``` bash
jupyter notebook
```

Execute os notebooks na seguinte sequência:

1.  `notebook/01_EDA.ipynb` --- análise exploratória, preparação e
    geração dos conjuntos de treinamento e validação.
2.  `notebook/02_ML.ipynb` --- pipelines, validação cruzada, comparação
    e avaliação dos modelos.
3.  `notebook/01_EDA_figuras.ipynb` e `notebook/02_ML_figuras.ipynb` ---
    notebooks auxiliares para salvar as figuras em PNG no diretório
    `docs/figuras/`.

Os notebooks auxiliares de figuras reproduzem as etapas correspondentes
dos notebooks originais para gerar os arquivos de imagem. O notebook de
ML executa novamente as etapas de modelagem necessárias à produção de
suas figuras.

> Os caminhos e nomes dos arquivos devem ser mantidos conforme a
> estrutura do projeto. Caso a organização local seja diferente, ajuste
> os caminhos de leitura nos notebooks.

## Relatório

O relatório completo, com descrição dos procedimentos, resultados,
figuras, discussão e limitações, está disponível em:

[`docs/relatorio_geral.md`](docs/relatorio_geral.md)

As figuras utilizadas no relatório estão armazenadas em `docs/figuras/`.

## Tecnologias utilizadas

-   Python
-   Jupyter Notebook
-   Pandas e NumPy
-   Matplotlib e Seaborn
-   SciPy
-   Scikit-learn
-   XGBoost

## Considerações finais

O projeto documenta um fluxo de Ciência de Dados que abrange
entendimento dos dados, análise exploratória, preparação, validação
cruzada, comparação de modelos, interpretação e avaliação final.

Os resultados devem ser compreendidos dentro dos limites da base e da
variável-alvo disponíveis. A aplicação em contexto clínico exigiria
esclarecimento da origem dos rótulos e validação independente, além de
avaliação por profissionais habilitados.
