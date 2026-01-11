# Home.py
import streamlit as st
import utils
import os

st.set_page_config(page_title="Yassir RH", page_icon="🟣", layout="wide")

# Initialisation
utils.init_db()
utils.apply_style()

if 'user' not in st.session_state:
    st.session_state.user = None

# LOGIQUE LOGIN
if st.session_state.user is None:
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown("<br><h1 style='color:#6c1ddb; text-align:center;'>Yassir People</h1>", unsafe_allow_html=True)
        if os.path.exists(utils.LOGO_FILE):
            st.image(utils.LOGO_FILE, use_container_width=True)
            
        with st.form("login_form"):
            u = st.text_input("Identifiant")
            p = st.text_input("Mot de passe", type="password")
            submitted = st.form_submit_button("Se Connecter", type="primary")
            
            if submitted:
                df = utils.load_data(utils.USERS_FILE)
                if 'is_active' in df.columns:
                    usr = df[(df['username']==u) & (df['password']==p) & (df['is_active']==True)]
                else:
                    usr = df[(df['username']==u) & (df['password']==p)]
                
                if not usr.empty:
                    st.session_state.user = usr.iloc[0]
                    st.rerun()
                else:
                    st.error("Identifiants incorrects")
else:
    # SI DÉJÀ CONNECTÉ
    st.title(f"👋 Bienvenue, {st.session_state.user['full_name']}")
    st.info("👈 Utilisez le menu à gauche pour naviguer.")
    
    st.write("---")
    if st.button("Se déconnecter"):
        st.session_state.user = None
        st.rerun()
