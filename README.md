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
## Estrutura do projeto 
### **Execução**

- ETL e processamento de dados
- Seleção de features para EDA
- EDA
- Engenharia de features
- Treinamento do modelo, SHAP e decisão de negócio
- MLflow e Streamlit
- Conjunto de teste

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
- Registro e Versionamento com MLflow

---

## 🧾 Transparência e Responsabilidade

- As explicações apresentadas são **descritivas**, baseadas em padrões estatísticos aprendidos pelo modelo.
- Métricas por perfil demográfico **não implicam causalidade nem viés**, sendo utilizadas apenas para monitoramento.
- O modelo **não substitui análise humana**, atuando como ferramenta de apoio à decisão.

---

## 🏦 Decisão de Negócio Adotada

Após análise das métricas e simulação de impacto financeiro, foi definida uma política de crédito com foco na redução de perdas por inadimplência.

A estratégia adotada prioriza:

- Maximizar o Recall da Classe 1 (inadimplentes)
- Reduzir a concessão de crédito para clientes de alto risco
- Aceitar redução controlada na taxa de aprovação para proteger o resultado financeiro

O threshold final foi definido em **0.12**, adotando uma política deliberadamente conservadora.

A decisão prioriza a **máxima captura possível de clientes inadimplentes (Classe 1)**, mesmo que isso implique redução na taxa de aprovação.

Essa estratégia foi adotada porque, no contexto analisado, **o custo de conceder crédito a um inadimplente é significativamente superior ao custo de negar crédito a um adimplente**.

Portanto, a política de crédito implementada privilegia proteção contra perdas financeiras, aceitando aumento controlado na rejeição de clientes de baixo risco como mecanismo de mitigação.

Essa decisão está totalmente documentada no notebook técnico do projeto.

## 💰 Simulação de Impacto Financeiro

No cenário analisado, o custo de conceder crédito a um inadimplente é significativamente superior ao lucro obtido com um cliente adimplente.

Para fins de simulação, foram consideradas as seguintes premissas:

- Volume analisado: 10.000 solicitações de crédito
- Taxa média de inadimplência: 20%
- Ticket médio por operação: R$ 5.000
- Perda média por inadimplente: R$ 4.000
- Lucro médio por cliente adimplente: R$ 800

**Sem aplicação de modelo preditivo, os 2.000 clientes inadimplentes seriam aprovados, gerando:**

2.000 × R$ 4.000 = R$ 8.000.000 em perdas estimadas.

**Com o modelo implementado e recall de 82% para a classe inadimplente:**

- 1.640 inadimplentes seriam bloqueados
- 360 ainda receberiam crédito

Perda estimada:
360 × R$ 4.000 = R$ 1.440.000

**Redução de perdas:**
R$ 8.000.000 − R$ 1.440.000 = R$ 6.560.000

**Considerando uma rejeição adicional de clientes adimplentes (estimativa de R$ 1.200.000 em lucro não capturado), o ganho líquido estimado permanece positivo:**

Impacto financeiro líquido aproximado: + R$ 5.360.000

**Conclusão**

A política adotada (threshold = 0.12) privilegia a mitigação de perdas financeiras, refletindo uma estratégia conservadora de concessão de crédito.

Mesmo com redução na taxa de aprovação, a simulação indica que a diminuição da inadimplência supera o lucro não capturado, resultando em impacto financeiro líquido positivo.

*Os valores apresentados representam uma simulação ilustrativa para demonstrar impacto financeiro potencial.*


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
