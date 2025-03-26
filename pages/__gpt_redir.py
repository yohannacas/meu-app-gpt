import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore
import json

# 🔹 Inicializar Firebase
if not firebase_admin._apps:
    cred_dict = json.loads(st.secrets["firebase_credentials"])
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 🔎 Pegar todos os documentos da coleção de sessões ativas
docs = db.collection("active_sessions").stream()

# Se houver pelo menos uma sessão ativa, libera o acesso
acesso_liberado = False
for doc in docs:
    acesso_liberado = True
    break

GPT_URL = "https://chatgpt.com/g/g-XGtq9fsBf-vincent-pro-view"

if acesso_liberado:
    st.success("✅ Login autorizado.")
    st.markdown("### 👇 Acesse seu GPT na nova aba:")
    st.markdown(
        f'<a href="{GPT_URL}" target="_blank">🧠 👉 Abrir GPT Customizado</a>',
        unsafe_allow_html=True
    )
    st.info("Caso o botão não funcione, copie e cole este link manualmente:")
    st.code(GPT_URL)
else:
    st.error("🚫 Acesso não autorizado.")
    st.markdown('[🔐 Voltar para o login](../)', unsafe_allow_html=True)
