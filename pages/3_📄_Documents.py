import streamlit as st
import utils

st.set_page_config(page_title="Documents", page_icon="📄", layout="wide")
utils.apply_style()
utils.check_auth()

st.title("📄 Générateur de Documents")
user = st.session_state.user

target_user = user
if user['role'] == 'admin':
    users_db = utils.load_data(utils.USERS_FILE)
    choice = st.selectbox("Collaborateur :", users_db['username'].tolist())
    target_user = users_db[users_db['username'] == choice].iloc[0]

doc_type = st.selectbox("Type", ["Attestation de Travail", "Attestation de Salaire"])

if st.button("Générer PDF"):
    pdf_bytes = utils.create_pdf(target_user, doc_type)
    st.download_button("Télécharger PDF", pdf_bytes, f"{doc_type}.pdf", "application/pdf")
