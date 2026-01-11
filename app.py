import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
from fpdf import FPDF

# --- CONFIGURATION ---
st.set_page_config(page_title="Yassir RH Platform", layout="wide", page_icon="🟣")

DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.csv")
REQUESTS_FILE = os.path.join(DATA_DIR, "requests.csv")
LOGO_FILE = "logo.png"  # Assurez-vous d'avoir une image nommée ainsi

# --- MOTEUR PDF (YASSIR BRANDING) ---
class YassirPDF(FPDF):
    def header(self):
        # Bandeau Violet Yassir
        self.set_fill_color(108, 29, 219)
        self.rect(0, 0, 210, 35, 'F')
        
        # Logo
        if os.path.exists(LOGO_FILE):
            self.image(LOGO_FILE, 10, 8, 30)
        else:
            self.set_font('Arial', 'B', 20)
            self.set_text_color(255, 255, 255)
            self.text(10, 25, "YASSIR")

        self.set_font('Arial', 'B', 15)
        self.set_text_color(255, 255, 255)
        self.cell(0, 15, 'DOCUMENT ADMINISTRATIF', 0, 1, 'R')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Yassir Maroc - Genere le {datetime.now().strftime("%d/%m/%Y")}', 0, 0, 'C')

def create_pdf_doc(user_data, doc_type):
    pdf = YassirPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Titre
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(108, 29, 219)
    pdf.cell(0, 10, doc_type.upper(), 0, 1, 'C')
    pdf.ln(10)
    
    # Corps du texte
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=12)
    
    # Conversion safe des données pour éviter les erreurs
    u_name = str(user_data.get('full_name', ''))
    u_dob = str(user_data.get('dob', ''))
    u_addr = str(user_data.get('address', ''))
    u_mat = str(user_data.get('username', ''))
    u_job = str(user_data.get('job_title', ''))
    u_start = str(user_data.get('start_date', ''))
    u_fam = str(user_data.get('family_status', ''))
    
    text = f"""Je soussigné(e), Représentant des Ressources Humaines de Yassir Maroc,

Certifie que :
M./Mme {u_name}
Né(e) le : {u_dob}
Adresse : {u_addr}
Matricule : {u_mat}

Occupe le poste de : {u_job}
Depuis le : {u_start}
Situation Familiale : {u_fam}

"""
    if doc_type == "Attestation de Salaire":
        text += f"Perçoit un salaire brut mensuel de : {user_data.get('base_salary', 0)} MAD\n"
    
    text += """
Ce document est délivré à l'intéressé(e) pour servir et valoir ce que de droit.

Fait à Casablanca.
"""
    pdf.multi_cell(0, 8, text)
    
    pdf.ln(20)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(100)
    pdf.cell(0, 10, "Direction des Ressources Humaines", 0, 1)
    
    return pdf.output(dest='S').encode('latin-1', 'replace')

def create_timesheet_pdf(user_data, week_start, hours_worked, absences):
    pdf = YassirPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"FEUILLE DE TEMPS HEBDOMADAIRE", 0, 1, 'C')
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 8, f"Collaborateur : {user_data.get('full_name', '')} | Semaine du : {week_start}", 0, 1, 'L')
    pdf.ln(5)
    
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(100, 10, "Total Heures Travaillees", 1, 0, 'L', 1)
    pdf.cell(90, 10, f"{hours_worked} Heures", 1, 1, 'C')
    
    pdf.cell(100, 10, "Objectif Hebdomadaire", 1, 0, 'L', 1)
    status = "ATTEINT" if hours_worked >= 40 else "NON ATTEINT"
    pdf.set_text_color(0, 128, 0) if hours_worked >= 40 else pdf.set_text_color(255, 0, 0)
    pdf.cell(90, 10, f"40 Heures ({status})", 1, 1, 'C')
    pdf.set_text_color(0, 0, 0)
    
    pdf.ln(5)
    pdf.multi_cell(0, 8, f"Absences / Remarques :\n{absences if absences else 'R.A.S'}", 1)
    
    pdf.ln(20)
    pdf.set_font("Arial", "I", 10)
    pdf.cell(95, 40, "Signature du Collaborateur :", 1, 0)
    pdf.cell(95, 40, "Validation Manager :", 1, 1)
    
    return pdf.output(dest='S').encode('latin-1', 'replace')

# --- GESTION DONNÉES ET MIGRATION ---
def init_db():
    if not os.path.exists(DATA_DIR): os.makedirs(DATA_DIR)
    
    # Colonnes complètes requises pour le nouveau système
    required_cols = ["username","password","role","full_name","department","cp_balance","job_title","base_salary","start_date","rib","address","dob","family_status","phone","contract_type","is_active"]
    
    reset_needed = False
    
    # Vérifier si le fichier existe
    if os.path.exists(USERS_FILE):
        try:
            df = pd.read_csv(USERS_FILE)
            # Si les colonnes ne matchent pas (ancien fichier), on reset
            if not set(required_cols).issubset(df.columns):
                reset_needed = True
        except:
            reset_needed = True
    else:
        reset_needed = True

    if reset_needed:
        # Création de la DB Admin par défaut
        df = pd.DataFrame(columns=required_cols)
        df.loc[0] = ["admin","admin123","admin","Admin RH","RH",0,"DRH",0,"2020-01-01","000","Casa","1980-01-01","Célibataire","0600000000","CDI",True]
        df.to_csv(USERS_FILE, index=False)
        # On force le rechargement pour éviter les erreurs de cache
        if 'user' in st.session_state:
            st.session_state.user = None

    if not os.path.exists(REQUESTS_FILE):
        pd.DataFrame(columns=["id", "username", "type", "date_request", "start_date", "end_date", "status", "details"]).to_csv(REQUESTS_FILE, index=False)

def load_data(file_path):
    # Charge les données, si erreur, réinitialise
    try: 
        return pd.read_csv(file_path)
    except: 
        init_db() 
        return pd.read_csv(file_path)

def save_data(df, file_path): df.to_csv(file_path, index=False)

def login(u, p):
    df = load_data(USERS_FILE)
    # Vérifie username, password et si le compte est actif
    user = df[(df['username'] == u) & (df['password'] == p)]
    if not user.empty:
        # Vérification optionnelle de la colonne is_active si elle existe
        if 'is_active' in user.columns and str(user.iloc[0]['is_active']) == 'False':
            return None
        return user.iloc[0]
    return None

# --- INTERFACES ---

def sidebar_menu(role):
    with st.sidebar:
        st.title("🟣 Yassir RH")
        st.caption(f"Connecté: {st.session_state.user['full_name']}")
        
        if role == 'admin':
            menu = st.radio("Menu Admin", ["Gestion Profils", "Documents RH", "Suivi Planning"], key="admin_menu")
        else:
            menu = st.radio("Menu Collaborateur", ["Mes Documents", "Mon Planning", "Mes Infos"], key="user_menu")
            
        st.divider()
        if st.button("Se déconnecter"):
            st.session_state.user = None
            st.rerun()
    return menu

def page_admin_profils():
    st.header("👥 Gestion des Profils & Contrats")
    users = load_data(USERS_FILE)
    
    tab1, tab2 = st.tabs(["Ajouter un Collaborateur", "Modifier / Départ"])
    
    with tab1:
        with st.form("new_user_form"):
            st.subheader("Infos Personnelles")
            c1, c2, c3 = st.columns(3)
            nu_user = c1.text_input("Identifiant (Login)")
            nu_pass = c2.text_input("Mot de passe")
            nu_nom = c3.text_input("Nom Prénom")
            
            c1, c2 = st.columns(2)
            nu_addr = c1.text_input("Adresse")
            nu_tel = c2.text_input("Téléphone")
            
            c1, c2 = st.columns(2)
            nu_dob = c1.date_input("Date de Naissance", value=date(1995,1,1))
            nu_fam = c2.selectbox("Situation Familiale", ["Célibataire", "Marié(e)", "Divorcé(e)"])
            
            st.subheader("Infos Contrat")
            c1, c2, c3 = st.columns(3)
            nu_dept = c1.selectbox("Département", ["IT", "Ops", "Finance", "Marketing"])
            nu_job = c2.text_input("Poste")
            nu_type = c3.selectbox("Type Contrat", ["CDI", "CDD", "Anapec", "Stage"])
            
            c1, c2 = st.columns(2)
            nu_sal = c1.number_input("Salaire Base (MAD)", 5000)
            nu_start = c2.date_input("Date Début", value=date.today())
            
            if st.form_submit_button("✅ Créer le profil"):
                # Vérif doublon
                if nu_user in users['username'].values:
                    st.error("Cet identifiant existe déjà.")
                else:
                    new_row = {
                        "username": nu_user, "password": nu_pass, "role": "user",
                        "full_name": nu_nom, "department": nu_dept, "cp_balance": 18,
                        "job_title": nu_job, "base_salary": nu_sal, "start_date": nu_start,
                        "rib": "", "address": nu_addr, "dob": nu_dob, 
                        "family_status": nu_fam, "phone": nu_tel, "contract_type": nu_type,
                        "is_active": True
                    }
                    users = pd.concat([users, pd.DataFrame([new_row])], ignore_index=True)
                    save_data(users, USERS_FILE)
                    st.success("Collaborateur ajouté !")
                    st.rerun()
                
    with tab2:
        # Affiche seulement les actifs
        active_users = users
        if 'is_active' in users.columns:
            active_users = users[users['is_active'] != False]
            
        st.dataframe(active_users)
        
        user_to_edit = st.selectbox("Sélectionner un collaborateur", active_users[active_users['role']!='admin']['username'].unique())
        if user_to_edit:
            col_act1, col_act2 = st.columns(2)
            if col_act1.button("⚠️ Marquer comme Sortie / Démission"):
                users.loc[users['username'] == user_to_edit, 'is_active'] = False
                save_data(users, USERS_FILE)
                st.warning(f"Le profil {user_to_edit} a été désactivé.")
                st.rerun()

def page_doc_generation(is_admin=False):
    st.header("📄 Générateur de Documents")
    users = load_data(USERS_FILE)
    target_user = st.session_state.user
    
    if is_admin:
        st.info("Mode Admin")
        choice = st.selectbox("Collaborateur", users['username'].tolist())
        target_user = users[users['username'] == choice].iloc[0]
    
    st.write(f"**Génération pour : {target_user['full_name']}**")
    doc_type = st.selectbox("Document", ["Attestation de Travail", "Attestation de Salaire"])
    
    if st.button("Générer PDF"):
        try:
            pdf_bytes = create_pdf_doc(target_user, doc_type)
            st.success("Document généré !")
            st.download_button(
                label="📥 Télécharger le PDF",
                data=pdf_bytes,
                file_name=f"{doc_type}_{target_user['username']}.pdf",
                mime='application/pdf'
            )
        except Exception as e:
            st.error(f"Erreur PDF : {e}")

def page_planning_timesheet(is_admin=False):
    st.header("🗓️ Planning & Timesheet")
    users = load_data(USERS_FILE)
    target_user = st.session_state.user
    
    if is_admin:
        choice = st.selectbox("Collaborateur", users['username'].tolist(), key="plan_user")
        target_user = users[users['username'] == choice].iloc[0]

    st.subheader(f"Feuille de temps : {target_user['full_name']}")
    
    with st.form("timesheet_form"):
        col1, col2 = st.columns(2)
        week_start = col1.date_input("Lundi de la semaine", value=date.today())
        hours = col2.number_input("Heures effectuées", min_value=0, max_value=80, value=40)
        absences_txt = st.text_area("Absences / Remarques")
        
        if st.form_submit_button("Générer PDF"):
            pdf_bytes = create_timesheet_pdf(target_user, week_start, hours, absences_txt)
            st.download_button(
                label="📥 Télécharger Feuille de Temps",
                data=pdf_bytes,
                file_name=f"Timesheet_{week_start}.pdf",
                mime='application/pdf'
            )

# --- ROUTAGE PRINCIPAL ---

# 1. Vérification BDD
init_db()

# 2. Gestion Session
if 'user' not in st.session_state:
    st.session_state.user = None

# 3. Logique d'affichage
if st.session_state.user is None:
    # --- PAGE DE LOGIN ---
    st.markdown("<h1 style='color:#6c1ddb; text-align:center;'>Yassir People</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        u = st.text_input("Identifiant")
        p = st.text_input("Mot de passe", type="password")
        if st.button("Se connecter", type="primary"):
            usr = login(u, p)
            if usr is not None:
                st.session_state.user = usr
                st.rerun()
            else:
                st.error("Identifiants incorrects")
else:
    # --- APP CONNECTÉE ---
    user_role = st.session_state.user['role']
    
    # Appel du Menu (la fonction doit être définie AVANT)
    menu_choice = sidebar_menu(user_role)
    
    if user_role == 'admin':
        if menu_choice == "Gestion Profils":
            page_admin_profils()
        elif menu_choice == "Documents RH":
            page_doc_generation(is_admin=True)
        elif menu_choice == "Suivi Planning":
            page_planning_timesheet(is_admin=True)
    else:
        if menu_choice == "Mes Documents":
            page_doc_generation(is_admin=False)
        elif menu_choice == "Mon Planning":
            page_planning_timesheet(is_admin=False)
        elif menu_choice == "Mes Infos": 
            st.title("Mon Dossier")
            # Convertit en dictionnaire pour affichage propre
            st.json(st.session_state.user.to_dict())
