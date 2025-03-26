import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore
import json

# 🔹 Inicializar Firebase (caso ainda não esteja)
if not firebase_admin._apps:
    cred_dict = json.loads(st.secrets["firebase_credentials"])
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 🔹 Obter e-mail da sessão (se houver)
email = st.session_state.get("email")

# 🔹 Verificar se a sessão está ativa no Firestore
acesso_liberado = False
if email:
    try:
        user = auth.get_user_by_email(email)
        user_id = user.uid
        doc = db.collection("active_sessions").document(user_id).get()
        if doc.exists:
            acesso_liberado = True
    except:
        acesso_liberado = False

# 🔹 Redirecionar ou bloquear
GPT_URL = "https://chatgpt.com/g/g-XGtq9fsBf-vincent-pro-view"

if acesso_liberado:
    st.markdown("🔁 Redirecionando para o GPT...")
    st.markdown(f'<meta http-equiv="refresh" content="1; url={GPT_URL}" />', unsafe_allow_html=True)
else:
    st.error("🚫 Acesso não autorizado.")
    st.markdown('[🔐 Voltar para o login](../)', unsafe_allow_html=True)
