
import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
import shap
import matplotlib.pyplot as plt

from preprocessing import preprocess

# ===============================
# Streamlit config
# ===============================
st.set_page_config(
    page_title="Modelo de Risco de Crédito",
    layout="wide"
)

# ===============================
# Load artifacts
# ===============================
with open("credit_risk_model_bundle.pkl", "rb") as f:
    artifacts = pickle.load(f)

model = artifacts["model"]
DEFAULT_THRESHOLD = float(artifacts["threshold"])

# ===============================
# Feature → Negócio
# ===============================
FEATURE_MAPPING = {
    "PAYMENT_RATIO_MEAN": "Comprometimento da renda influenciou a decisão de risco",
    "POS_CNT_INSTALMENT_FUTURE_MEAN": "Quantidade de parcelamentos futuros impactou o risco",
    "EXT_SOURCE_3": "Score externo teve influência relevante na avaliação do risco",
    "EXT_SOURCE_2": "Score externo contribuiu para a decisão de crédito",
    "EXT_SOURCE_1": "Comportamento capturado por score externo afetou o risco",
    "AMT_CREDIT": "Valor do crédito solicitado impactou a decisão",
    "AMT_ANNUITY": "Valor da parcela mensal influenciou o risco",
    "DAYS_EMPLOYED": "Histórico de vínculo empregatício impactou a decisão",
    "OWN_CAR_AGE": "Indicador patrimonial contribuiu para avaliação do risco",
    "INST_NULL_INSTALMENT_NUMBER_COUNT": (
        "Ausência de informações em contratos parcelados anteriores influenciou a decisão"
    ),
    "PREV_CNT_PAYMENT_MEAN": (
        "Comportamento médio de pagamentos em contratos anteriores impactou o risco"
    ),
    "PREV_REFUSAL_RATE": (
        "Histórico de recusas anteriores influenciou a avaliação do risco"
    ),
    "CODE_GENDER": (
        "Padrões estatísticos associados ao perfil demográfico influenciaram a decisão"
    )
}

def explicar_feature(feature, shap_value):
    base = FEATURE_MAPPING.get(
        feature,
        f"O comportamento da variável {feature} influenciou a decisão"
    )
    direcao = "aumentando o risco" if shap_value > 0 else "reduzindo o risco"
    return f"{base}, {direcao}."

# ===============================
# UI
# ===============================
st.title("Modelo de Risco de Crédito")
st.markdown("**Transformando risco em decisões claras e orientadas a lucro.**")
st.divider()

file = st.file_uploader("Envie um arquivo CSV para análise", type="csv")

threshold = st.slider(
    "Escolha o corte de risco",
    min_value=0.01,
    max_value=0.99,
    value=DEFAULT_THRESHOLD,
    step=0.01
)

# ===============================
# Sidebar - Negócio
# ===============================
st.sidebar.header("Parâmetros de Negócio")

ticket_medio = st.sidebar.number_input(
    "Ticket médio do crédito (R$)",
    min_value=1000,
    value=15000,
    step=1000
)

prejuizo_medio = st.sidebar.number_input(
    "Prejuízo médio por inadimplência (R$)",
    min_value=1000,
    value=12000,
    step=1000
)

# ===============================
# Upload e previsão
# ===============================
if file:
    df_raw = pd.read_csv(file)
    st.subheader("Prévia dos dados")
    st.dataframe(df_raw.head())

    if st.button("Executar Previsão"):
        df_proc = preprocess(df_raw)
        proba = model.predict(df_proc)

        df = df_raw.copy()
        df["PROB_DEFAULT"] = proba
        df["TARGET_PRED"] = (proba >= threshold).astype(int)
        df["DECISION"] = df["TARGET_PRED"].map({1: "NEGADO", 0: "APROVADO"})

        st.session_state["df"] = df
        st.session_state["df_proc"] = df_proc
        st.session_state["threshold"] = threshold

# ===============================
# Resultados
# ===============================
if "df" in st.session_state:

    df = st.session_state["df"]
    df_proc = st.session_state["df_proc"]

    st.subheader("Resultado da Previsão")
    st.dataframe(df)

    st.info(
        f"📌 Regra: probabilidade ≥ {st.session_state['threshold']:.2f} → NEGADO"
    )

    # ===============================
    # KPIs
    # ===============================
    aprovados = df[df["TARGET_PRED"] == 0]
    negados = df[df["TARGET_PRED"] == 1]
    total_clientes = len(df)

    st.subheader("📊 Visão Executiva")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Clientes", total_clientes)
    col2.metric("Clientes Aprovados", len(aprovados))
    col3.metric("Clientes Negados", len(negados))

    receita_bruta = len(aprovados) * ticket_medio
    prejuizo_estimado = len(aprovados) * prejuizo_medio * 0.25
    lucro_liquido = receita_bruta - prejuizo_estimado

    col4, col5, col6 = st.columns(3)
    col4.metric("Receita Bruta (R$)", f"{receita_bruta:,.0f}")
    col5.metric("Prejuízo Estimado (R$)", f"{prejuizo_estimado:,.0f}")
    col6.metric("Lucro Líquido (R$)", f"{lucro_liquido:,.0f}")

    pie_df = pd.DataFrame({
        "Categoria": ["Lucro Líquido", "Prejuízo", "Receita Não Capturada"],
        "Valor (R$)": [
            max(lucro_liquido, 0),
            prejuizo_estimado,
            len(negados) * ticket_medio
        ]
    })

    fig_pie = px.pie(
    pie_df,
    names="Categoria",
    values="Valor (R$)",
    hole=0.45,
    title="Distribuição Financeira das Decisões",
    color="Categoria",
    color_discrete_map={
        "Receita Não Capturada": "#0b3c5d",  # azul escuro
        "Lucro Líquido": "#7fc97f",          # verde claro
        "Prejuízo": "#d62728"                # vermelho
    }
    )

    st.plotly_chart(fig_pie, use_container_width=True)

    # ===============================
    # KPI - Aprovação vs Negação por Gênero
    # ===============================
    st.subheader("⚖️ Aprovações e Negações por Gênero")

    if "CODE_GENDER" in df.columns:

        df_genero = df.copy()

        df_genero["GENERO"] = df_genero["CODE_GENDER"].map({
            "M": "Homem",
            "F": "Mulher"
        }).fillna("Não informado")

        kpi_genero = (
            df_genero
            .groupby(["GENERO", "DECISION"])
            .size()
            .reset_index(name="Quantidade")
        )

        fig_genero = px.bar(
            kpi_genero,
            x="GENERO",
            y="Quantidade",
            color="DECISION",
            barmode="group",
            text="Quantidade",
            title="Distribuição de Decisões por Gênero",
            color_discrete_map={
                "NEGADO": "#d62728",
                "APROVADO": "#7fc97f"
            }
            )

        fig_genero.update_layout(
            xaxis_title="Gênero",
            yaxis_title="Quantidade de Clientes",
            legend_title="Decisão",
            height=400
        )

        st.plotly_chart(fig_genero, use_container_width=True)

        st.caption(
            "⚠️ Este indicador é descritivo. Diferenças observadas não implicam, "
            "isoladamente, viés do modelo."
        )

    else:
        st.warning("A coluna CODE_GENDER não está presente no dataset.")


    # ===============================
    # EXPLICABILIDADE
    # ===============================
    st.subheader("🧠 Explicação da Decisão")

    explainer = shap.TreeExplainer(model)
    shap_values = explainer(df_proc)

    cliente_idx = st.number_input(
        "Escolha o índice do cliente",
        min_value=0,
        max_value=len(df_proc) - 1,
        step=1
    )

    shap_row = shap_values[cliente_idx]

    shap_df = pd.DataFrame({
        "feature": shap_row.feature_names,
        "shap_value": shap_row.values
    })

    TOP_N = 8

    top_reasons = (
        shap_df
        .assign(abs_shap=lambda x: x["shap_value"].abs())
        .sort_values("abs_shap", ascending=False)
        .head(TOP_N)
    )

    st.markdown("### 📌 Principais fatores que influenciaram a decisão")

    for _, row in top_reasons.iterrows():
        st.write(f"- **{explicar_feature(row['feature'], row['shap_value'])}**")

    # ===============================
    # CONCLUSÃO FINAL
    # ===============================
    decisao_cliente = df.loc[cliente_idx, "DECISION"]

    st.subheader("🧾 Conclusão da Análise")

    if decisao_cliente == "NEGADO":
        st.warning(
            "A solicitação foi **negada** porque a combinação dos principais fatores "
            "indicou **risco elevado de inadimplência**, especialmente relacionados a "
            "capacidade de pagamento, histórico de crédito e comportamento financeiro."
        )
    else:
        st.success(
            "A solicitação foi **aprovada** porque os principais indicadores apontam "
            "**capacidade de pagamento adequada**, histórico favorável e risco controlado "
            "segundo os critérios do modelo."
        )

    # ===============================
    # SHAP TÉCNICO
    # ===============================
    with st.expander("🔍 Detalhamento técnico (SHAP)"):
        fig, ax = plt.subplots()
        shap.plots.waterfall(
            shap_row,
            max_display=8,
            show=False
        )
        st.pyplot(fig, bbox_inches="tight")
        plt.close(fig)

    # ===============================
    # Explicação geral
    # ===============================
    with st.expander("📘 Como o modelo toma decisões"):
        st.markdown("""
        **1️⃣ O modelo estima o risco de inadimplência.**
        Utilizamos LightGBM com foco em reduzir perdas.

        **2️⃣ O threshold define a política de crédito.**
        Quanto menor, mais conservadora a decisão.

        **3️⃣ A decisão final é explicável e rastreável.**
        Cada decisão é acompanhada dos fatores mais relevantes.

        **4️⃣ SHAP garante transparência e auditabilidade.**
        """)
