# Aplicação Streamlit — Classificação demonstrativa de hipotireoidismo

Esta pasta contém a interface interativa do projeto **Diagnóstico de Hipotireoidismo**. A aplicação permite informar características demográficas, clínicas e laboratoriais e consultar a classificação e a saída probabilística do pipeline final de Random Forest.

A aplicação foi desenvolvida para demonstração educacional do fluxo de inferência. Ela não realiza treinamento, comparação de algoritmos ou avaliação dos modelos durante sua execução.

## Arquivo principal

- `app.py`: interface Streamlit, validação dos campos, organização dos dados de entrada e execução da inferência.
- `imagem/app_imagem1.png`: captura de tela da interface utilizada na documentação do projeto.

## Como a aplicação funciona

Ao iniciar, o aplicativo carrega o artefato serializado em:

```text
models/modelo_hipotireoidismo.joblib
```

O arquivo contém o pipeline treinado, a identificação do modelo e a lista ordenada dos preditores esperados. A aplicação utiliza essa lista para montar a entrada com as mesmas colunas e ordem utilizadas no treinamento.

### Informações disponíveis na interface

**Perfil e informações clínicas**
- Idade;
- Sexo registrado;
- Origem do encaminhamento;
- Uso de tiroxina;
- Investigação de hipotireoidismo e hipertireoidismo;
- Outras informações clínicas presentes entre os preditores do modelo.

**Resultados laboratoriais**
- TSH;
- T3;
- TT4;
- T4U;
- FTI.

Os resultados laboratoriais são opcionais. A interface aceita ponto ou vírgula como separador decimal. Os indicadores de realização dos exames (`measured`) são preenchidos de acordo com a presença ou ausência do respectivo resultado.

Campos binários são convertidos para o padrão textual `t`/`f` utilizado no treinamento. Campos não informados são representados como ausentes e tratados pelas etapas de imputação do pipeline.

## Interpretação do resultado

A interface apresenta a classe prevista e a saída de `predict_proba` para a classe positiva:

- **N — classe positiva:** registro rotulado como hipotireoidismo na variável `binaryClass`;
- **P — classe negativa:** registro rotulado como não hipotireoidismo.

O percentual exibido corresponde à estimativa do classificador de pertencimento à classe N, com base nos padrões aprendidos durante o treinamento. Não representa uma probabilidade clínica individual validada, não deve ser interpretado como risco pessoal e não constitui diagnóstico.

Os valores iniciais e os perfis de demonstração servem para explorar o comportamento do classificador. Não representam faixas laboratoriais de referência, critérios diagnósticos ou recomendações de saúde.

## Estrutura esperada do projeto

O diretório `app/` deve permanecer na raiz do projeto, no mesmo nível de `models/`, `src/` e `treinar_modelo.py`:

```text
Diagnostico_hipotireoidismo/
├── app/
│   ├── app.py
│   ├── README.md
│   └── imagem/
│       └── app_imagem1.png
├── models/
│   └── modelo_hipotireoidismo.joblib
├── src/
│   └── preprocessing.py
└── treinar_modelo.py
```

A aplicação resolve o caminho do artefato a partir da localização de `app.py`. Por isso, execute o comando a partir da raiz do projeto e mantenha a estrutura de diretórios.

## Pré-requisitos

- Python no ambiente utilizado para treinar/exportar o modelo;
- Streamlit;
- Joblib;
- NumPy e Pandas;
- Scikit-learn em versão compatível com a utilizada na serialização do artefato;
- Demais bibliotecas exigidas pelo pipeline salvo.

Recomenda-se utilizar o mesmo ambiente Conda no treinamento e na execução da aplicação, evitando incompatibilidades de versões ao carregar o arquivo `joblib`.

## Executar a aplicação

Na raiz do projeto, ative o ambiente Python configurado e execute:

```bash
conda activate data_science
python -m streamlit run app/app.py
```

O Streamlit apresentará um endereço local, normalmente `http://localhost:8501`, para abrir a aplicação no navegador.

## Gerar ou atualizar o modelo

A geração do artefato não é realizada nesta pasta. Ela é responsabilidade do script `treinar_modelo.py`, localizado na raiz do projeto.

Na raiz do projeto:

```bash
python treinar_modelo.py
```

O script utiliza `data/df_treino.csv` e exporta o artefato para `models/modelo_hipotireoidismo.joblib`. Depois de gerar o artefato, inicie novamente a aplicação com o comando Streamlit.

## Materiais relacionados

- `../notebook/`: notebooks de análise exploratória e modelagem;
- `../src/`: funções auxiliares e transformações compartilhadas;
- `../models/`: artefato serializado do modelo final;
- `../docs/relatorio_geral.md`: relatório com metodologia, resultados e limitações do estudo;
- `../README.md`: apresentação geral do projeto.

---

**Aviso:** ferramenta exclusivamente educacional e demonstrativa. Não utilizar para diagnóstico, decisão clínica ou substituição de avaliação por profissional de saúde.
