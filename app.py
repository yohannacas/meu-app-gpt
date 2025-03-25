import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore
import time
import webbrowser
import uuid
import json

if not firebase_admin._apps:
    cred_dict = json.loads(st.secrets["firebase_credentials"])
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

# 🔹 Conectar ao Firestore
db = firestore.client()

# 🔹 Configuração do Streamlit
st.set_page_config(page_title="Login - Processador Jurídico", layout="wide")
st.title("🔐 Login para Acessar o GPT")

# 🔹 Campos de entrada para login
email = st.text_input("E-mail")
password = st.text_input("Senha", type="password")

# 🔹 URL do GPT Customizado
GPT_URL = "https://chatgpt.com/g/g-XGtq9fsBf-vincent-pro-view"

# Após login bem-sucedido:
st.success(f"✅ Login bem-sucedido! Bem-vindo, {user.email}")
st.markdown(f"""<meta http-equiv="refresh" content="2; url={GPT_URL}" />""", unsafe_allow_html=True)

# 🔹 Botão de login
if st.button("Entrar"):
    if email and password:
        try:
            # 🔹 Verificar se o usuário existe no Firebase
            user = auth.get_user_by_email(email)
            user_id = user.uid  # ID único do usuário no Firebase

            # 🔹 Checar se o usuário já tem uma sessão ativa no Firestore
            user_doc = db.collection("active_sessions").document(user_id).get()

            if user_doc.exists:
                st.error("⚠️ Esta conta já está sendo usada em outro dispositivo. Faça logout antes de entrar novamente.")
            else:
                # 🔹 Criar uma sessão única com UUID
                session_id = str(uuid.uuid4())

                # 🔹 Salvar a sessão no Firestore
                db.collection("active_sessions").document(user_id).set({
                    "session_id": session_id,
                    "email": email,
                    "timestamp": firestore.SERVER_TIMESTAMP
                })

                st.success(f"✅ Login bem-sucedido! Bem-vindo, {user.email}")
                time.sleep(2)
                webbrowser.open_new(GPT_URL)

        except Exception as e:
            st.error(f"❌ Erro: {e}")

    else:
        st.warning("⚠️ Por favor, preencha todos os campos.")

# 🔹 Botão de logout
if st.button("Sair"):
    if email:
        try:
            user = auth.get_user_by_email(email)
            user_id = user.uid

            # 🔹 Remover a sessão do Firestore
            db.collection("active_sessions").document(user_id).delete()
            st.success("🚪 Logout realizado com sucesso!")

        except Exception as e:
            st.error(f"❌ Erro ao sair: {e}")
