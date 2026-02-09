# Projeto de Análise e Previsão de Risco de Crédito

## 📊 Modelo de Risco de Crédito — Home Credit

Aplicação interativa para **análise e decisão de risco de crédito**, desenvolvida com foco em **minimização de perdas financeiras** e **transparência nas decisões**.  
O projeto utiliza **Machine Learning (LightGBM)** aplicado ao dataset **Home Credit**, integrando métricas técnicas e indicadores de negócio em um único produto.

---

## 🧠 Contexto do Problema

Em operações de crédito, **os custos associados a decisões incorretas não são simétricos**:

- ❌ **Aprovar um cliente inadimplente** pode gerar **perdas financeiras diretas**, impacto no fluxo de caixa e aumento da inadimplência.
- ⚠️ **Negar crédito a um cliente adimplente** representa apenas **custo de oportunidade** (receita não capturada).

Dado esse cenário, **o erro mais crítico é o falso negativo**  
> *(classificar um inadimplente como adimplente)*

Por isso, o projeto foi desenvolvido com **prioridade na detecção correta de clientes inadimplentes**.

---

## 🎯 Métrica-Chave do Projeto

A métrica principal adotada é o **Recall da Classe 1 (Inadimplentes)**.

- **Recall Classe 1 alto** → menor probabilidade de conceder crédito a clientes de alto risco  
- Aceita-se uma redução controlada na taxa de aprovação para **proteger o resultado financeiro**

O *threshold* de decisão é **ajustável**, permitindo simular políticas de crédito mais ou menos conservadoras.

---

## 🎯 Objetivo do Projeto

Desenvolver uma **aplicação prática e interpretável de risco de crédito** que:

- Identifique clientes com **alto risco de inadimplência**
- Priorize **redução de prejuízo financeiro**
- Traduza decisões técnicas em **impacto de negócio**
- Ofereça **transparência e rastreabilidade** das decisões do modelo
- Permita **simulação de políticas de crédito** via ajuste de threshold

---

## 🔍 Funcionalidades da Aplicação

- 📥 Upload de base CSV para análise em lote  
- 📈 Predição de probabilidade de inadimplência por cliente  
- 🎚️ Threshold configurável (política de risco)  
- 📊 KPIs executivos:
  - Receita bruta
  - Prejuízo estimado
  - Lucro líquido
  - Receita não capturada
- ⚖️ Análise descritiva de aprovações e negações por gênero  
- 🧠 Explicabilidade individual com **SHAP**
- 📌 Tradução técnica → linguagem de negócio

---

## 🧪 Modelo e Abordagem Técnica

- Algoritmo: **LightGBM**
- Tipo de problema: **Classificação binária**
- Classe 1: **Inadimplente**
- Otimização focada em:
  - Recall da Classe 1
  - Ajuste de threshold pós-treinamento
- Pipeline de pré-processamento reproduzível
- Modelo e artefatos versionados via pickle
- Regstro e Versionamento com MLflow

---

## 🧾 Transparência e Responsabilidade

- As explicações apresentadas são **descritivas**, baseadas em padrões estatísticos aprendidos pelo modelo.
- Métricas por perfil demográfico **não implicam causalidade nem viés**, sendo utilizadas apenas para monitoramento.
- O modelo **não substitui análise humana**, atuando como ferramenta de apoio à decisão.

---

## 🚀 Aplicação Online

👉 **Acesse o app:**  
*(link do Streamlit Cloud será adicionado após o deploy)*

---

## 🧰 Stack Utilizada

- Python
- Pandas / NumPy
- LightGBM
- Scikit-learn
- SHAP
- Streamlit
- Plotly
- Matplotlib
- MLflow

---

## 📌 Próximos Passos

- Monitoramento de performance em produção
- Análise de *drift* de dados
- Evolução para API desacoplada

---

## 👤 Autor

**Matheus Mata**  
Projeto desenvolvido para fins de estudo, portfólio e aplicação prática em risco de crédito.
