import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st


# Estrutura esperada:
# Diagnostico_hipotireoidismo/
# ├── models/modelo_hipotireoidismo.joblib
# └── app/app.py
PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models" / "modelo_hipotireoidismo.joblib"

# Atualize este endereço quando o repositório estiver publicado no GitHub.
GITHUB_URL = "https://github.com/albertoakel/EBAC/tree/master/Diagnostico_hipotireoidismo"

st.set_page_config(
    page_title="Projeto — Classificação de hipotireoidismo",
    page_icon="🧪",
    layout="wide",
)


# Identidade visual: interface editorial, limpa e contemporânea.
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

    :root {
        --ink: #17243a;
        --muted: #66758b;
        --line: #e5eaf1;
        --paper: #f5f7fb;
        --blue: #3157d5;
        --blue-soft: #edf2ff;
        --teal: #087f8c;
    }
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        color: var(--ink);
    }
    .stApp { background: var(--paper); }
    [data-testid="stHeader"] { background: rgba(245,247,251,.92); }
    .block-container {
        max-width: 1180px;
        padding-top: 2.2rem;
        padding-bottom: 4rem;
    }
    h1, h2, h3, h4 {
        font-family: 'Manrope', sans-serif !important;
        letter-spacing: -0.035em;
        color: var(--ink);
    }
    h1 { font-size: 2.35rem !important; font-weight: 800 !important; }
    h2 { font-size: 1.35rem !important; font-weight: 800 !important; }
    h3 { font-size: 1.05rem !important; font-weight: 700 !important; }
    p, label, .stCaption { color: var(--muted); }
    .hero {
        background: linear-gradient(120deg, #142746 0%, #203e70 58%, #3157a4 100%);
        border-radius: 22px;
        padding: 2.15rem 2.3rem;
        color: white;
        margin: 0 0 1.4rem 0;
        box-shadow: 0 14px 35px rgba(26,48,88,.14);
    }
    .hero-kicker {
        text-transform: uppercase;
        letter-spacing: .16em;
        font-size: .72rem;
        font-weight: 700;
        color: #b8c9ee;
        margin-bottom: .65rem;
    }
    .hero-title {
        font-family: 'Manrope', sans-serif;
        font-size: 2rem;
        line-height: 1.18;
        font-weight: 800;
        color: #fff;
        margin: 0 0 .55rem 0;
    }
    .hero-subtitle {
        color: #d7e2f5;
        font-size: .98rem;
        max-width: 720px;
        line-height: 1.6;
        margin: 0;
    }
    .eyebrow {
        color: var(--blue);
        font-size: .72rem;
        text-transform: uppercase;
        letter-spacing: .13em;
        font-weight: 800;
        margin-bottom: .25rem;
    }
    .section-note {
        color: var(--muted);
        font-size: .9rem;
        margin-top: -.35rem;
        margin-bottom: 1rem;
    }
    .result-panel {
        background: white;
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 1.35rem 1.5rem;
        min-height: 150px;
        box-shadow: 0 5px 18px rgba(22,39,68,.04);
    }
    .result-label {
        color: var(--muted);
        font-size: .78rem;
        font-weight: 700;
        letter-spacing: .06em;
        text-transform: uppercase;
        margin-bottom: .5rem;
    }
    .result-value {
        font-family: 'Manrope', sans-serif;
        color: var(--ink);
        font-size: 2.1rem;
        line-height: 1.15;
        font-weight: 800;
    }
    .result-description {
        color: var(--muted);
        font-size: .86rem;
        margin-top: .5rem;
        line-height: 1.45;
    }
    .stButton > button, .stFormSubmitButton > button {
        border-radius: 10px;
        min-height: 3rem;
        font-weight: 700;
        border: 0;
    }
    .stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] {
        background: var(--blue);
    }
    div[data-testid="stExpander"] {
        border: 1px solid var(--line);
        border-radius: 12px;
        background: white;
    }
    div[data-testid="stForm"] {
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 1.3rem 1.4rem 1rem 1.4rem;
        background: white;
    }
    div[data-testid="stAlert"] { border-radius: 12px; }
    .footer {
        border-top: 1px solid var(--line);
        padding-top: 1.2rem;
        margin-top: 2.5rem;
        color: var(--muted);
        font-size: .82rem;
    }
    a { color: var(--blue) !important; font-weight: 600; }
    @media (max-width: 700px) {
        .block-container { padding: 1rem 1rem 3rem 1rem; }
        .hero { padding: 1.5rem; border-radius: 16px; }
        .hero-title { font-size: 1.55rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner="Carregando modelo...")
def carregar_artefato(caminho: str):
    return joblib.load(caminho)


def valor_binario(opcao: str):
    """Converte a resposta da interface para o padrão t/f usado no treinamento."""
    conversao = {
        "Sim": "t",
        "Não": "f",
        "Não informado": np.nan,
    }
    return conversao[opcao]


def converter_resultado_numerico(texto: str, nome: str, erros: list):
    """Converte campo laboratorial opcional, aceitando vírgula decimal."""
    texto = texto.strip()
    if not texto:
        return np.nan
    try:
        valor = float(texto.replace(",", "."))
        if not np.isfinite(valor):
            raise ValueError
        return valor
    except ValueError:
        erros.append(f"{nome}: informe um número válido ou deixe o campo vazio.")
        return np.nan


def criar_entrada(features, dados):
    """Monta uma linha com as mesmas colunas e ordem usadas no treinamento."""
    entrada = {coluna: np.nan for coluna in features}
    for coluna, valor in dados.items():
        if coluna in entrada:
            entrada[coluna] = valor
    return pd.DataFrame([entrada], columns=features)


st.markdown(
    """
    <section class="hero">
      <div class="hero-kicker">Projeto aplicado · Ciência de Dados</div>
      <div class="hero-title">Análise preditiva de hipotireoidismo</div>
      <p class="hero-subtitle">
        Uma demonstração interativa de classificação com aprendizado de máquina.
        Informe os dados disponíveis para observar a estimativa probabilística
        produzida pelo modelo.
      </p>
    </section>
    """,
    unsafe_allow_html=True,
)

st.warning(
    "**Importante:** ferramenta acadêmica e demonstrativa. A probabilidade exibida "
    "é produzida por um classificador treinado para reproduzir os rótulos do conjunto "
    "de dados. Não corresponde a uma probabilidade clínica individual, não confirma "
    "nem descarta doença e não substitui avaliação profissional."
)



if not MODEL_PATH.exists():
    st.error(f"Modelo não encontrado em: `{MODEL_PATH}`")
    st.info(
        "Execute `python treinar_modelo.py` na raiz do projeto para gerar o artefato "
        "em `models/modelo_hipotireoidismo.joblib`."
    )
    st.stop()

try:
    artefato = carregar_artefato(str(MODEL_PATH))
    modelo = artefato["model"]
    features = artefato["features"]
except Exception as exc:
    st.error(f"Não foi possível carregar o modelo: {exc}")
    st.stop()

if not hasattr(modelo, "predict_proba"):
    st.error("O artefato carregado não disponibiliza predict_proba().")
    st.stop()

# with st.expander("Detalhes técnicos do modelo", expanded=False):
#     st.write(f"**Modelo:** {artefato.get('model_name', 'Não informado')}")
#     st.write(f"**Número de preditores:** {len(features)}")
#     data_exportacao = artefato.get("created_at_utc")
#     if data_exportacao:
#         st.write(f"**Exportado em (UTC):** {data_exportacao}")
#     st.caption(
#         "A aplicação carrega o pipeline já treinado. Nenhum treinamento ou ajuste "
#         "de parâmetros é realizado durante a inferência."
#     )

#st.markdown('<div class="eyebrow">Entrada de dados</div>', unsafe_allow_html=True)
st.markdown("## Informações para análise")
st.markdown(
    '<p class="section-note">Preencha os campos que conhecer. Informações não disponíveis '
    'podem permanecer em branco.</p>',
    unsafe_allow_html=True,
)

with st.form("formulario_classificacao"):
    st.markdown("### 01 · Perfil e informações clínicas")
    col1, col2, col3 = st.columns(3)

    with col1:
        idade = st.number_input("Idade (anos)", min_value=0, max_value=120, value=40, step=1)
        sexo = st.selectbox("Sexo registrado", ["Não informado", "F", "M"], index=1)

    with col2:
        origem = st.selectbox(
            "Origem do encaminhamento",
            ["Não informado", "SVHC", "other", "SVI", "STMW", "SVHD"],
            index=1,
        )
        uso_tiroxina = st.selectbox("Uso de tiroxina", ["Não informado", "Sim", "Não"], index=2)

    with col3:
        investigacao_hipo = st.selectbox(
            "Investigação de hipotireoidismo", ["Não informado", "Sim", "Não"], index=2
        )
        investigacao_hiper = st.selectbox(
            "Investigação de hipertireoidismo", ["Não informado", "Sim", "Não"], index=2
        )

    with st.expander("Outras informações clínicas", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            investigacao_tiroxina = st.selectbox(
                "Investigação relacionada à tiroxina", ["Não informado", "Sim", "Não"], index=2
            )
            medicacao_antitireoidiana = st.selectbox(
                "Uso de medicação antitireoidiana", ["Não informado", "Sim", "Não"], index=2
            )
            doente = st.selectbox("Registro de doença atual", ["Não informado", "Sim", "Não"], index=2)
            gravidez = st.selectbox("Registro de gravidez", ["Não informado", "Sim", "Não"], index=2)
        with c2:
            cirurgia = st.selectbox(
                "Histórico de cirurgia da tireoide", ["Não informado", "Sim", "Não"], index=2
            )
            tratamento_i131 = st.selectbox(
                "Tratamento com I131", ["Não informado", "Sim", "Não"], index=2
            )
            litio = st.selectbox("Registro de uso de lítio", ["Não informado", "Sim", "Não"], index=2)
        with c3:
            bocio = st.selectbox("Registro de bócio", ["Não informado", "Sim", "Não"], index=2)
            tumor = st.selectbox("Registro de tumor", ["Não informado", "Sim", "Não"], index=2)
            psic = st.selectbox(
                "Registro de condição psiquiátrica", ["Não informado", "Sim", "Não"], index=2
            )

    st.markdown("### 02 · Resultados laboratoriais")
    st.caption("Informe os resultados disponíveis. Aceita ponto ou vírgula como separador decimal.")

    labs = {}
    lab_cols = st.columns(5)
    for coluna, rotulo, col in zip(
        ["TSH", "T3", "TT4", "T4U", "FTI"],
        ["TSH", "T3", "TT4", "T4U", "FTI"],
        lab_cols,
    ):
        with col:
            valores_exemplo = {
                "TSH": "2.0",
                "T3": "2.0",
                "TT4": "100",
                "T4U": "1.0",
                "FTI": "100",
            }
            labs[coluna] = st.text_input(
                rotulo,
                value=valores_exemplo[coluna],
                help=(
                    f"Valor ilustrativo de {rotulo}. Edite conforme desejar; "
                    "apague o campo se não houver informação."
                ),
            )

    enviar = st.form_submit_button(
        "Calcular estimativa", type="primary", use_container_width=True
    )

if enviar:
    erros = []
    dados = {
        "age": float(idade),
        "sex": np.nan if sexo == "Não informado" else sexo,
        "referral source": np.nan if origem == "Não informado" else origem,
        "on thyroxine": valor_binario(uso_tiroxina),
        "query on thyroxine": valor_binario(investigacao_tiroxina),
        "on antithyroid medication": valor_binario(medicacao_antitireoidiana),
        "sick": valor_binario(doente),
        "pregnant": valor_binario(gravidez),
        "thyroid surgery": valor_binario(cirurgia),
        "I131 treatment": valor_binario(tratamento_i131),
        "query hypothyroid": valor_binario(investigacao_hipo),
        "query hyperthyroid": valor_binario(investigacao_hiper),
        "lithium": valor_binario(litio),
        "goitre": valor_binario(bocio),
        "tumor": valor_binario(tumor),
        "psych": valor_binario(psic),
    }

    for coluna, texto in labs.items():
        resultado = converter_resultado_numerico(texto, coluna, erros)
        dados[coluna] = resultado
        # Os indicadores measured fazem parte dos preditores do treinamento.
        dados[f"{coluna} measured"] = "t" if texto.strip() else "f"

    # Confere se o formulário cobre os preditores do artefato; não deixa uma
    # coluna desconhecida passar silenciosamente sem ser percebida.
    colunas_sem_campo = [
        coluna for coluna in features
        if coluna not in dados
    ]

    if erros:
        for erro in erros:
            st.error(erro)
    elif colunas_sem_campo:
        st.error(
            "O formulário não contempla todos os preditores do modelo: "
            + ", ".join(colunas_sem_campo)
        )
        st.info(
            "Confira se o artefato corresponde ao treinamento deste projeto e se "
            "o formulário está sincronizado com a versão do modelo."
        )
    else:
        X_novo = criar_entrada(features, dados)
        try:
            classe = int(modelo.predict(X_novo)[0])
            probabilidades = modelo.predict_proba(X_novo)[0]
            classes_modelo = list(modelo.classes_)
            indice_n = classes_modelo.index(1)
            probabilidade_n = float(probabilidades[indice_n])
        except Exception as exc:
            st.error(f"Falha ao executar a inferência: {exc}")
            st.stop()

        st.markdown('<div class="eyebrow">Resultado da análise</div>', unsafe_allow_html=True)
        st.markdown("## Estimativa do modelo")
        st.markdown(
            '<p class="section-note">Resultado calculado a partir dos dados informados '
            'e dos padrões aprendidos durante o treinamento.</p>',
            unsafe_allow_html=True,
        )

        probabilidade_p = float(probabilidades[classes_modelo.index(0)])
        res1, res2 = st.columns([1, 1.35], gap="medium")
        with res1:
            classe_label = "N · Positiva" if classe == 1 else "P · Negativa"
            descricao_classe = (
                "O registro foi classificado na categoria positiva do conjunto de dados."
                if classe == 1
                else "O registro foi classificado na categoria negativa do conjunto de dados."
            )
            st.markdown(
                f"""
                <div class="result-panel">
                  <div class="result-label">Classe atribuída</div>
                  <div class="result-value">{classe_label}</div>
                  <div class="result-description">{descricao_classe}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with res2:
            st.markdown(
                f"""
                <div class="result-panel">
                  <div class="result-label">Probabilidade estimada para a classe N</div>
                  <div class="result-value">{probabilidade_n:.1%}</div>
                  <div class="result-description">
                    Estimativa do modelo de pertencimento à classe rotulada como
                    hipotireoidismo no conjunto de dados.
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.progress(
            probabilidade_n,
            text=f"Classe N: {probabilidade_n:.1%}  ·  Classe P: {probabilidade_p:.1%}",
        )
        st.caption(
            "P = classe negativa (registro rotulado como não hipotireoidismo) · "
            "N = classe positiva (registro rotulado como hipotireoidismo)."
        )

        st.info(
            f"Para os dados fornecidos, o modelo estima **{probabilidade_n:.1%} de "
            "probabilidade de pertencimento à classe N** e "
            f"**{probabilidade_p:.1%} para a classe P**. Esses valores descrevem a "
            "saída do classificador, não uma chance clínica validada para o indivíduo."
        )

        with st.expander("Como interpretar esta estimativa?"):
            st.markdown(
                """
                O modelo foi treinado para reconhecer padrões associados aos rótulos
                presentes na base de dados. A probabilidade é calculada pelo próprio
                classificador e não foi apresentada aqui como risco clínico calibrado.
                O desempenho observado no estudo não garante o mesmo resultado em
                outras populações ou contextos de atendimento.
                """
            )


with st.expander("Sobre o projeto", expanded=False):
    st.markdown(
        """
        O projeto percorre as etapas de exploração, preparação dos dados, comparação
        de algoritmos e avaliação de modelos para reproduzir a variável-alvo
        `binaryClass` do conjunto **Hypothyroid**.

        **Interpretação dos rótulos originais**
        - **N — classe positiva:** registro rotulado como hipotireoidismo.
        - **P — classe negativa:** registro rotulado como não hipotireoidismo.

        A aplicação utiliza o pipeline final de Random Forest. A saída probabilística
        indica o quanto o modelo estima que o registro informado se enquadra na classe
        N, segundo os padrões aprendidos nos dados utilizados no estudo.
        """
    )
    st.markdown("**Documentação e código**")
    st.markdown(
        "- Relatório: `docs/relatorio_geral.pdf` e `docs/relatorio_geral.md`."
    )
    if "SEU_USUARIO" not in GITHUB_URL:
        st.markdown(f"- [Repositório no GitHub]({GITHUB_URL})")
    else:
        st.caption("O endereço do GitHub será disponibilizado quando o repositório for publicado.")

with st.expander("Detalhes técnicos do modelo", expanded=False):
    st.write(f"**Modelo:** {artefato.get('model_name', 'Não informado')}")
    st.write(f"**Número de preditores:** {len(features)}")
    data_exportacao = artefato.get("created_at_utc")
    if data_exportacao:
        st.write(f"**Exportado em (UTC):** {data_exportacao}")
    st.caption(
        "A aplicação carrega o pipeline já treinado. Nenhum treinamento ou ajuste "
        "de parâmetros é realizado durante a inferência.")
st.markdown(
    """
    <div class="footer">
      <strong>Projeto acadêmico · EBAC · Ciência de Dados</strong><br>
      Classificação demonstrativa com aprendizado de máquina ·
      Os resultados não constituem diagnóstico ou orientação médica.
    </div>
    """,
    unsafe_allow_html=True,
)
if "SEU_USUARIO" not in GITHUB_URL:
    st.markdown(f"[Código-fonte no GitHub]({GITHUB_URL})")
