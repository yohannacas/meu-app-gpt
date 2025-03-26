import streamlit as st

# 🔹 URL do GPT Customizado
GPT_URL = "https://chatgpt.com/g/g-XGtq9fsBf-vincent-pro-view"

# 🔐 Verifica se o usuário está autenticado
if st.session_state.get("autenticado"):
    st.markdown("🔁 Redirecionando para o GPT...")
    st.markdown(f'<meta http-equiv="refresh" content="1; url={GPT_URL}" />', unsafe_allow_html=True)
else:
    st.error("🚫 Acesso não autorizado.")
    st.markdown('[🔐 Voltar para o login](./)', unsafe_allow_html=True)
