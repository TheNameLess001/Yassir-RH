import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Portail RH Yassir", layout="wide", page_icon="🏢")

# --- GESTION DES DONNÉES (PERSISTENCE CSV) ---
DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.csv")
REQUESTS_FILE = os.path.join(DATA_DIR, "requests.csv")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Initialisation des fichiers CSV s'ils n'existent pas
if not os.path.exists(USERS_FILE):
    df_users = pd.DataFrame(columns=["username", "password", "role", "full_name", "department", "cp_balance"])
    # Création d'un admin par défaut (A CHANGER EN PROD)
    df_users.loc[0] = ["admin", "admin123", "admin", "Admin RH", "RH", 0]
    df_users.to_csv(USERS_FILE, index=False)

if not os.path.exists(REQUESTS_FILE):
    pd.DataFrame(columns=["id", "username", "type", "date_request", "start_date", "end_date", "status", "details"]).to_csv(REQUESTS_FILE, index=False)

# --- FONCTIONS UTILITAIRES ---
def load_data(file_path):
    return pd.read_csv(file_path)

def save_data(df, file_path):
    df.to_csv(file_path, index=False)

def login(username, password):
    users = load_data(USERS_FILE)
    user = users[(users['username'] == username) & (users['password'] == password)]
    if not user.empty:
        return user.iloc[0]
    return None

# --- INTERFACES ---

def admin_interface():
    st.title("🔧 Espace Administrateur RH")
    
    tab1, tab2, tab3 = st.tabs(["Gestion Personnel", "Import CSV", "Suivi des Demandes"])

    with tab1:
        st.subheader("Ajouter un collaborateur manuellement")
        with st.form("add_user_form"):
            col1, col2 = st.columns(2)
            new_user = col1.text_input("Nom d'utilisateur")
            new_pass = col2.text_input("Mot de passe", type="password")
            new_name = col1.text_input("Nom Complet")
            new_dept = col2.selectbox("Département", ["IT", "Opérations", "Marketing", "Finance"])
            new_cp = st.number_input("Solde CP Initial", min_value=0, value=18)
            submitted = st.form_submit_button("Créer Compte")
            
            if submitted:
                users = load_data(USERS_FILE)
                if new_user in users['username'].values:
                    st.error("Cet utilisateur existe déjà.")
                else:
                    new_row = {"username": new_user, "password": new_pass, "role": "user", "full_name": new_name, "department": new_dept, "cp_balance": new_cp}
                    users = pd.concat([users, pd.DataFrame([new_row])], ignore_index=True)
                    save_data(users, USERS_FILE)
                    st.success(f"Utilisateur {new_name} créé !")

        st.subheader("Liste des collaborateurs")
        st.dataframe(load_data(USERS_FILE))

    with tab2:
        st.subheader("Importation en masse (CSV)")
        st.info("Format requis : username, password, role, full_name, department, cp_balance")
        uploaded_file = st.file_uploader("Choisir un fichier CSV", type="csv")
        if uploaded_file is not None:
            try:
                new_data = pd.read_csv(uploaded_file)
                current_data = load_data(USERS_FILE)
                # Fusion simple (pour l'exemple)
                combined = pd.concat([current_data, new_data]).drop_duplicates(subset=['username'])
                save_data(combined, USERS_FILE)
                st.success("Données importées avec succès !")
            except Exception as e:
                st.error(f"Erreur lors de l'import : {e}")

    with tab3:
        st.subheader("Toutes les demandes")
        reqs = load_data(REQUESTS_FILE)
        
        # Filtres
        filter_status = st.selectbox("Filtrer par statut", ["Tous", "En attente", "Approuvé", "Rejeté"])
        if filter_status != "Tous":
            reqs = reqs[reqs['status'] == filter_status]
            
        st.dataframe(reqs)
        
        # Action sur une demande
        st.write("---")
        st.write("**Traiter une demande**")
        req_id = st.text_input("ID de la demande à traiter")
        col_act1, col_act2 = st.columns(2)
        if col_act1.button("✅ Approuver"):
            df_reqs = load_data(REQUESTS_FILE)
            df_reqs.loc[df_reqs['id'] == req_id, 'status'] = 'Approuvé'
            save_data(df_reqs, REQUESTS_FILE)
            st.success(f"Demande {req_id} approuvée.")
            st.rerun()
            
        if col_act2.button("❌ Rejeter"):
            df_reqs = load_data(REQUESTS_FILE)
            df_reqs.loc[df_reqs['id'] == req_id, 'status'] = 'Rejeté'
            save_data(df_reqs, REQUESTS_FILE)
            st.warning(f"Demande {req_id} rejetée.")
            st.rerun()

def user_interface(user_info):
    st.title(f"👋 Bienvenue, {user_info['full_name']}")
    st.info(f"Département : {user_info['department']} | Solde CP : {user_info['cp_balance']} jours")

    tab1, tab2 = st.tabs(["📅 Mes Congés & Absences", "📄 Demande de Documents"])

    with tab1:
        st.subheader("Planifier une absence / CP")
        with st.form("leave_form"):
            leave_type = st.selectbox("Type d'absence", ["Congé Payé (CP)", "Maladie", "Récupération", "Télétravail"])
            col1, col2 = st.columns(2)
            start_d = col1.date_input("Date de début")
            end_d = col2.date_input("Date de fin")
            reason = st.text_area("Motif / Commentaire")
            
            submit_leave = st.form_submit_button("Soumettre la demande")
            
            if submit_leave:
                reqs = load_data(REQUESTS_FILE)
                new_id = str(len(reqs) + 1).zfill(4) # ID simple: 0001, 0002
                new_req = {
                    "id": new_id,
                    "username": user_info['username'],
                    "type": leave_type,
                    "date_request": datetime.now().strftime("%Y-%m-%d"),
                    "start_date": start_d,
                    "end_date": end_d,
                    "status": "En attente",
                    "details": reason
                }
                reqs = pd.concat([reqs, pd.DataFrame([new_req])], ignore_index=True)
                save_data(reqs, REQUESTS_FILE)
                st.success("Demande envoyée au service RH !")

        st.subheader("Historique de mes demandes")
        all_reqs = load_data(REQUESTS_FILE)
        my_reqs = all_reqs[all_reqs['username'] == user_info['username']]
        st.table(my_reqs[['type', 'start_date', 'end_date', 'status']])

    with tab2:
        st.subheader("Demander un document administratif")
        doc_type = st.selectbox("Document souhaité", ["Attestation de travail", "Fiche de paie", "Attestation de salaire", "Domiciliation bancaire"])
        if st.button("Commander ce document"):
            reqs = load_data(REQUESTS_FILE)
            new_id = str(len(reqs) + 1).zfill(4)
            new_req = {
                "id": new_id,
                "username": user_info['username'],
                "type": f"Document: {doc_type}",
                "date_request": datetime.now().strftime("%Y-%m-%d"),
                "start_date": "-",
                "end_date": "-",
                "status": "En attente",
                "details": "Demande standard"
            }
            reqs = pd.concat([reqs, pd.DataFrame([new_req])], ignore_index=True)
            save_data(reqs, REQUESTS_FILE)
            st.success(f"La demande pour '{doc_type}' a été transmise.")

# --- MAIN APP LOGIC ---

if 'user' not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    # Page de Login
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("## Portail RH Yassir")
        username = st.text_input("Identifiant")
        password = st.text_input("Mot de passe", type="password")
        if st.button("Se connecter"):
            user = login(username, password)
            if user is not None:
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Identifiants incorrects")
else:
    # Sidebar Logout
    with st.sidebar:
        st.write(f"Connecté en tant que : **{st.session_state.user['username']}**")
        if st.button("Se déconnecter"):
            st.session_state.user = None
            st.rerun()

    # Router vers la bonne interface
    if st.session_state.user['role'] == 'admin':
        admin_interface()
    else:
        user_interface(st.session_state.user)
