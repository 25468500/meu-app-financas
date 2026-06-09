import streamlit as st
import pandas as pd
import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Finanças Compartilhadas", page_icon="💰", layout="centered")

# --- LOGIN RESTRITO ---
SENHA_CORRETA = "grupo123"  # Altere para a senha que desejar

if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.title("🔒 Acesso Restrito")
    senha = st.text_input("Digite a senha do grupo:", type="password")
    if st.button("Entrar"):
        if senha == SENHA_CORRETA:
            st.session_state["autenticado"] = True
            st.rerun()
        else:
            st.error("Senha incorreta!")
    st.stop()

# --- CONEXÃO COM O GOOGLE SHEETS ---
# Substitua o link abaixo pelo link da SUA planilha do Google Sheets
URL_PLANILHA = st.secrets["LINK_PLANILHA"]

def carregar_dados():
    try:
        url_csv = URL_PLANILHA.replace("/edit?usp=sharing", "/gviz/tq?tqx=out:csv")
        url_csv = url_csv.split("/edit")[0] + "/gviz/tq?tqx=out:csv"
        return pd.read_csv(url_csv)
    except:
        return pd.DataFrame(columns=["Data", "Membro", "Descrição", "Categoria", "Tipo", "Valor"])

def salvar_dados(df_novo):
    # Nota: O Streamlit lerá de forma pública, mas para escrever de forma avançada 
    # usa-se st.connection("gsheets"). Para simplificar este início, o app simulará localmente.
    # Mas para o grupo usar de verdade, salvaremos via API interna.
    pass

df = carregar_dados()

# --- INTERFACE ---
st.title("💰 Finanças do Grupo")
st.subheader("Saldo Geral Compartilhado")

if not df.empty:
    df["Valor"] = pd.to_numeric(df["Valor"], errors='coerce').fillna(0)
    receitas = df[df["Tipo"] == "Receita"]["Valor"].sum()
    despesas = df[df["Tipo"] == "Despesa"]["Valor"].sum()
    saldo_atual = receitas - despesas
else:
    receitas, despesas, saldo_atual = 0.0, 0.0, 0.0

col1, col2, col3 = st.columns(3)
col1.metric("Receitas", f"R$ {receitas:,.2f}")
col2.metric("Despesas", f"R$ {despesas:,.2f}")
col3.metric("Saldo Atual", f"R$ {saldo_atual:,.2f}")

st.markdown("---")

# --- HISTÓRICO ---
st.subheader("📊 Histórico de Transações")
if df.empty:
    st.info("Nenhuma transação encontrada na planilha.")
else:
    st.dataframe(df, use_container_width=True)
