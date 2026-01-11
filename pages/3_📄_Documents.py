import streamlit as st
import utils
from datetime import datetime

st.set_page_config(page_title="Documents RH", page_icon="📄", layout="wide")
utils.apply_style()
utils.check_auth()

st.title("📄 Espace Documents & Paie")
user = st.session_state.user

# --- SELECTION DU COLLABORATEUR (Si Admin) ---
target_user = user
if user['role'] == 'admin':
    users_db = utils.load_data(utils.USERS_FILE)
    st.info("Mode Admin : Génération pour un collaborateur")
    choice = st.selectbox("Sélectionner l'employé :", users_db['username'].tolist(), format_func=lambda x: f"{x} - {users_db[users_db['username']==x]['full_name'].values[0]}")
    target_user = users_db[users_db['username'] == choice].iloc[0]
else:
    st.write(f"Dossier de : **{user['full_name']}**")

st.markdown("---")

# --- ONGLETS ---
tab1, tab2 = st.tabs(["📜 Certificats & Attestations", "💰 Bulletins de Paie"])

with tab1:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Attestation de Travail")
        st.caption("Document officiel certifiant votre emploi actuel.")
        
        # Vérification des données manquantes importantes
        missing_data = []
        if str(target_user.get('cin','')) in ['nan', '', 'N/A']: missing_data.append("CIN")
        if str(target_user.get('cnss_number','')) in ['nan', '', 'N/A']: missing_data.append("Numéro CNSS")
        
        if missing_data and user['role'] == 'admin':
            st.warning(f"Données manquantes pour ce document : {', '.join(missing_data)}. Veuillez mettre à jour le profil.")
        
        if st.button("Générer l'Attestation de Travail"):
            pdf_bytes = utils.create_work_certificate(target_user)
            st.download_button(
                label="📥 Télécharger PDF",
                data=pdf_bytes,
                file_name=f"Attestation_Travail_{target_user['username']}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

with tab2:
    st.subheader("Historique de Paie")
    
    c1, c2 = st.columns(2)
    month_list = [datetime.now().strftime("%B %Y"), "Décembre 2025", "Novembre 2025"]
    selected_month = c1.selectbox("Choisir la période", month_list)
    
    if c2.button("Voir le Bulletin"):
        pdf_bytes = utils.create_payslip_pdf(target_user, selected_month)
        st.success(f"Bulletin de {selected_month} généré !")
        st.download_button(
            label="📥 Télécharger Bulletin de Paie",
            data=pdf_bytes,
            file_name=f"Bulletin_{target_user['username']}_{selected_month}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

# --- SECTION ADMIN : MISE A JOUR RAPIDE ---
if user['role'] == 'admin':
    st.markdown("---")
    with st.expander("🛠️ Mise à jour rapide des infos légales (CIN/CNSS)"):
        with st.form("quick_update"):
            new_cin = st.text_input("CIN", value=str(target_user.get('cin','')))
            new_cnss = st.text_input("CNSS", value=str(target_user.get('cnss_number','')))
            
            if st.form_submit_button("Sauvegarder"):
                df = utils.load_data(utils.USERS_FILE)
                idx = df[df['username'] == target_user['username']].index[0]
                df.at[idx, 'cin'] = new_cin
                df.at[idx, 'cnss_number'] = new_cnss
                utils.save_data(df, utils.USERS_FILE)
                st.success("Infos mises à jour ! Rechargez la page pour générer les documents.")
