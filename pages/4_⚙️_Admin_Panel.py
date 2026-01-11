import streamlit as st
import utils

st.set_page_config(page_title="Admin", page_icon="⚙️", layout="wide")
utils.apply_style()
utils.check_auth()

# Sécurité stricte : Si pas admin, on vire
if st.session_state.user['role'] != 'admin':
    st.error("Accès interdit.")
    st.stop()

st.title("⚙️ Administration RH")

tab1, tab2 = st.tabs(["👥 Gestion Utilisateurs", "📊 Données Globales"])

with tab1:
    df_users = utils.load_data(utils.USERS_FILE)
    st.dataframe(df_users)
    st.info("Pour ajouter un utilisateur, modifiez directement le CSV ou ajoutez un formulaire ici.")

with tab2:
    st.write("Statistiques globales (A implémenter)")
