import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

# --- CONFIGURATION ---
st.set_page_config(page_title="Yassir RH Platform", layout="wide", page_icon="🏢")

DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.csv")
REQUESTS_FILE = os.path.join(DATA_DIR, "requests.csv")

# --- MOTEUR DE PAIE MAROCAIN (SIMPLIFIÉ) ---
def calculate_moroccan_payroll(salary_base, start_date_str, primes_perf=0):
    try:
        # 1. Ancienneté
        start_date = datetime.strptime(str(start_date_str), "%Y-%m-%d").date()
        today = date.today()
        seniority_years = relativedelta(today, start_date).years
        
        rate_seniority = 0
        if seniority_years >= 25: rate_seniority = 0.25
        elif seniority_years >= 20: rate_seniority = 0.20
        elif seniority_years >= 12: rate_seniority = 0.15
        elif seniority_years >= 5: rate_seniority = 0.10
        elif seniority_years >= 2: rate_seniority = 0.05
        
        seniority_bonus = salary_base * rate_seniority
        
        # 2. Salaire Brut Global
        gross_salary = salary_base + seniority_bonus + primes_perf
        
        # 3. Cotisations Sociales (CNSS / AMO)
        # CNSS : 4.48% plafonné à 6000 MAD de base (donc max 268.8)
        base_cnss = min(gross_salary, 6000)
        cnss = base_cnss * 0.0448
        
        # AMO : 2.26% non plafonné
        amo = gross_salary * 0.0226
        
        # 4. Net Imposable (Base IGR)
        # Frais professionnels : 20% (ou 25% certains cas) plafonné à 2500/mois (30k/an)
        pro_expenses = min(gross_salary * 0.20, 2500)
        net_imposable = gross_salary - cnss - amo - pro_expenses
        
        # 5. Calcul IGR (Barème Mensuel 2024 approx)
        igr = 0
        if net_imposable <= 2500:
            igr = 0
        elif net_imposable <= 4166:
            igr = (net_imposable * 0.10) - 250
        elif net_imposable <= 5000:
            igr = (net_imposable * 0.20) - 666.67
        elif net_imposable <= 6666:
            igr = (net_imposable * 0.30) - 1166.67
        elif net_imposable <= 15000:
            igr = (net_imposable * 0.34) - 1433.33
        else:
            igr = (net_imposable * 0.38) - 2033.33
            
        igr = max(0, igr) # Pas d'impôt négatif
        
        # 6. Salaire Net
        net_salary = gross_salary - cnss - amo - igr
        
        return {
            "seniority_years": seniority_years,
            "seniority_rate": f"{int(rate_seniority*100)}%",
            "seniority_bonus": round(seniority_bonus, 2),
            "gross_salary": round(gross_salary, 2),
            "cnss": round(cnss, 2),
            "amo": round(amo, 2),
            "igr": round(igr, 2),
            "net_salary": round(net_salary, 2)
        }
    except Exception as e:
        return {"error": str(e)}

# --- GESTION DONNÉES ROBUSTE ---
def init_db():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    # Vérification Users
    if not os.path.exists(USERS_FILE) or os.stat(USERS_FILE).st_size == 0:
        df_users = pd.DataFrame(columns=["username", "password", "role", "full_name", "department", "cp_balance", "job_title", "base_salary", "start_date", "rib"])
        df_users.loc[0] = ["admin", "admin123", "admin", "Admin RH", "RH", 0, "DRH", 0, "2020-01-01", "000"]
        df_users.to_csv(USERS_FILE, index=False)

    # Vérification Requests
    if not os.path.exists(REQUESTS_FILE) or os.stat(REQUESTS_FILE).st_size == 0:
        pd.DataFrame(columns=["id", "username", "type", "date_request", "start_date", "end_date", "status", "details"]).to_csv(REQUESTS_FILE, index=False)

def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except pd.errors.EmptyDataError:
        # Si le fichier est corrompu/vide, on réinitialise
        init_db()
        return pd.read_csv(file_path)

def save_data(df, file_path):
    df.to_csv(file_path, index=False)

def login(username, password):
    users = load_data(USERS_FILE)
    user = users[(users['username'] == username) & (users['password'] == password)]
    return user.iloc[0] if not user.empty else None

# --- INTERFACES ---

def sidebar_menu(role):
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/WhatsApp_Inc._logo.svg/100px-WhatsApp_Inc._logo.svg.png", width=50) # Placeholder logo
        st.title("Yassir RH")
        st.write(f"👤 **{st.session_state.user['full_name']}**")
        st.write(f"🏷️ {st.session_state.user['job_title']}")
        st.divider()
        
        if role == 'admin':
            menu = st.radio("Navigation", ["Tableau de Bord", "Gestion Personnel", "Planning Global", "Simulateur Paie"])
        else:
            menu = st.radio("Navigation", ["Mon Espace", "Ma Fiche de Paie", "Mes Demandes"])
            
        st.divider()
        if st.button("Se déconnecter"):
            st.session_state.user = None
            st.rerun()
    return menu

def admin_interface(menu):
    if menu == "Tableau de Bord":
        st.title("📊 Vue d'ensemble")
        reqs = load_data(REQUESTS_FILE)
        pending = len(reqs[reqs['status'] == 'En attente'])
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Demandes en attente", pending, delta_color="inverse")
        col1.info("Action requise sur les demandes")
        
        st.subheader("Traiter les demandes")
        pending_reqs = reqs[reqs['status'] == 'En attente']
        if pending_reqs.empty:
            st.success("Aucune demande en attente.")
        else:
            for index, row in pending_reqs.iterrows():
                with st.expander(f"{row['type']} - {row['username']} ({row['date_request']})"):
                    st.write(f"**Détails:** {row['details']}")
                    st.write(f"**Dates:** {row['start_date']} au {row['end_date']}")
                    c1, c2 = st.columns(2)
                    if c1.button("✅ Approuver", key=f"app_{row['id']}"):
                        reqs.loc[reqs['id'] == row['id'], 'status'] = 'Approuvé'
                        save_data(reqs, REQUESTS_FILE)
                        st.rerun()
                    if c2.button("❌ Rejeter", key=f"rej_{row['id']}"):
                        reqs.loc[reqs['id'] == row['id'], 'status'] = 'Rejeté'
                        save_data(reqs, REQUESTS_FILE)
                        st.rerun()

    elif menu == "Gestion Personnel":
        st.title("👥 Base Collaborateurs")
        users = load_data(USERS_FILE)
        st.dataframe(users)
        
        with st.expander("➕ Ajouter un collaborateur"):
            with st.form("add_user"):
                c1, c2 = st.columns(2)
                new_user = c1.text_input("Username")
                new_pass = c2.text_input("Password")
                new_full = c1.text_input("Nom Complet")
                new_role = c2.selectbox("Role", ["user", "admin"])
                new_dept = c1.selectbox("Département", ["IT", "Ops", "Marketing", "Finance"])
                new_job = c2.text_input("Intitulé Poste")
                new_sal = c1.number_input("Salaire Base", value=10000)
                new_start = c2.date_input("Date Embauche")
                
                if st.form_submit_button("Créer"):
                    new_row = {
                        "username": new_user, "password": new_pass, "role": new_role,
                        "full_name": new_full, "department": new_dept, "cp_balance": 18,
                        "job_title": new_job, "base_salary": new_sal, 
                        "start_date": new_start, "rib": "0000"
                    }
                    users = pd.concat([users, pd.DataFrame([new_row])], ignore_index=True)
                    save_data(users, USERS_FILE)
                    st.success("Utilisateur ajouté !")
                    st.rerun()

    elif menu == "Planning Global":
        st.title("🗓️ Planning des Absences")
        reqs = load_data(REQUESTS_FILE)
        approved_leaves = reqs[(reqs['status'] == 'Approuvé') & (reqs['start_date'] != '-')]
        st.dataframe(approved_leaves[['username', 'type', 'start_date', 'end_date']], use_container_width=True)

    elif menu == "Simulateur Paie":
        st.title("🧮 Moteur de Paie & Social")
        users = load_data(USERS_FILE)
        selected_user = st.selectbox("Choisir un employé", users['username'].tolist())
        
        if selected_user:
            user_data = users[users['username'] == selected_user].iloc[0]
            st.write(f"**Calcul pour : {user_data['full_name']}** (Base: {user_data['base_salary']} MAD)")
            
            prime = st.number_input("Primes du mois (ex: Performance)", value=0)
            
            payroll = calculate_moroccan_payroll(user_data['base_salary'], user_data['start_date'], prime)
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Ancienneté", f"{payroll['seniority_years']} ans", f"+ {payroll['seniority_bonus']} MAD")
            c2.metric("Brut Global", f"{payroll['gross_salary']} MAD")
            c3.metric("Net à Payer", f"{payroll['net_salary']} MAD", delta_color="normal")
            
            st.subheader("Détail des cotisations")
            st.json(payroll)

def user_interface(menu, user_info):
    if menu == "Mon Espace":
        st.title(f"👋 Bonjour, {user_info['full_name']}")
        c1, c2, c3 = st.columns(3)
        c1.metric("Solde Congés", f"{user_info['cp_balance']} jours")
        c2.metric("Poste", user_info['job_title'])
        c3.metric("Ancienneté", f"{calculate_moroccan_payroll(user_info['base_salary'], user_info['start_date'])['seniority_years']} ans")
        
        st.subheader("Faire une demande")
        with st.form("req_form"):
            r_type = st.selectbox("Type", ["Congé Payé", "Télétravail", "Document RH"])
            d1 = st.date_input("Début (si applicable)")
            d2 = st.date_input("Fin (si applicable)")
            motif = st.text_area("Motif")
            if st.form_submit_button("Envoyer"):
                reqs = load_data(REQUESTS_FILE)
                new_id = str(len(reqs) + 1000)
                new_row = {
                    "id": new_id, "username": user_info['username'], "type": r_type,
                    "date_request": str(date.today()), "start_date": str(d1), 
                    "end_date": str(d2), "status": "En attente", "details": motif
                }
                reqs = pd.concat([reqs, pd.DataFrame([new_row])], ignore_index=True)
                save_data(reqs, REQUESTS_FILE)
                st.success("Envoyé !")

    elif menu == "Ma Fiche de Paie":
        st.title("💰 Ma Situation Salariale")
        st.info("Estimation basée sur la réglementation marocaine en vigueur.")
        
        payroll = calculate_moroccan_payroll(user_info['base_salary'], user_info['start_date'])
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("### Revenus")
            st.write(f"Salaire Base : **{user_info['base_salary']} MAD**")
            st.write(f"Prime Ancienneté ({payroll['seniority_rate']}) : **{payroll['seniority_bonus']} MAD**")
            st.markdown("---")
            st.write(f"**BRUT GLOBAL : {payroll['gross_salary']} MAD**")
            
        with col2:
            st.write("### Retenues")
            st.write(f"CNSS (4.48%) : {payroll['cnss']} MAD")
            st.write(f"AMO (2.26%) : {payroll['amo']} MAD")
            st.write(f"I.R. (Net) : {payroll['igr']} MAD")
            st.markdown("---")
            st.write(f"**TOTAL RETENUES : {round(payroll['cnss'] + payroll['amo'] + payroll['igr'], 2)} MAD**")
            
        st.success(f"### NET À PAYER : {payroll['net_salary']} MAD")

    elif menu == "Mes Demandes":
        st.title("Historique")
        reqs = load_data(REQUESTS_FILE)
        my_reqs = reqs[reqs['username'] == user_info['username']]
        st.dataframe(my_reqs)

# --- INIT & ROUTING ---
init_db()

if 'user' not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    st.markdown("## 🔐 Portail RH Yassir")
    u = st.text_input("Identifiant")
    p = st.text_input("Mot de passe", type="password")
    if st.button("Connexion"):
        usr = login(u, p)
        if usr is not None:
            st.session_state.user = usr
            st.rerun()
        else:
            st.error("Erreur d'authentification")
else:
    # Sidebar persistence
    menu_selection = sidebar_menu(st.session_state.user['role'])
    
    if st.session_state.user['role'] == 'admin':
        admin_interface(menu_selection)
    else:
        user_interface(menu_selection, st.session_state.user)
