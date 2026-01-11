import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from fpdf import FPDF
import base64

# --- CONFIGURATION ---
st.set_page_config(page_title="Yassir RH Platform", layout="wide", page_icon="🟣")

DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.csv")
REQUESTS_FILE = os.path.join(DATA_DIR, "requests.csv")
LOGO_FILE = "logo.png"  # Mettez votre logo Yassir ici

# --- MOTEUR PDF (YASSIR BRANDING) ---
class YassirPDF(FPDF):
    def header(self):
        # Bandeau Violet Yassir (RGB approx: 108, 29, 219)
        self.set_fill_color(108, 29, 219)
        self.rect(0, 0, 210, 35, 'F')
        
        # Logo (si le fichier existe)
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
        self.cell(0, 10, f'Yassir Maroc - Généré le {datetime.now().strftime("%d/%m/%Y")} - Page ' + str(self.page_no()), 0, 0, 'C')

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
    
    text = f"""Je soussigné(e), Représentant des Ressources Humaines de Yassir Maroc,

Certifie que :
M./Mme {user_data['full_name']}
Né(e) le : {user_data['dob']}
Adresse : {user_data['address']}
Matricule : {user_data['username']}

Occupe le poste de : {user_data['job_title']}
Depuis le : {user_data['start_date']}
Type de contrat : {user_data['contract_type']}
Situation Familiale : {user_data['family_status']}

"""
    if doc_type == "Attestation de Salaire":
        text += f"Perçoit un salaire brut mensuel de : {user_data['base_salary']} MAD\n"
    
    text += """
Ce document est délivré à l'intéressé(e) pour servir et valoir ce que de droit.

Fait à Casablanca.
"""
    pdf.multi_cell(0, 8, text)
    
    # Signature
    pdf.ln(20)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(100)
    pdf.cell(0, 10, "Direction des Ressources Humaines", 0, 1)
    
    return pdf.output(dest='S').encode('latin-1')

def create_timesheet_pdf(user_data, week_start, hours_worked, absences):
    pdf = YassirPDF()
    pdf.add_page()
    
    # Info Collaborateur
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"FEUILLE DE TEMPS HEBDOMADAIRE", 0, 1, 'C')
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 8, f"Collaborateur : {user_data['full_name']} | Semaine du : {week_start}", 0, 1, 'L')
    pdf.ln(5)
    
    # Tableau Heures
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(100, 10, "Total Heures Travaillées", 1, 0, 'L', 1)
    pdf.cell(90, 10, f"{hours_worked} Heures", 1, 1, 'C')
    
    pdf.cell(100, 10, "Objectif Hebdomadaire", 1, 0, 'L', 1)
    status = "ATTEINT" if hours_worked >= 40 else "NON ATTEINT"
    pdf.set_text_color(0, 128, 0) if hours_worked >= 40 else pdf.set_text_color(255, 0, 0)
    pdf.cell(90, 10, f"40 Heures ({status})", 1, 1, 'C')
    pdf.set_text_color(0, 0, 0)
    
    pdf.ln(5)
    pdf.multi_cell(0, 8, f"Déclaration des absences / congés sur la période :\n{absences if absences else 'Aucune absence déclarée.'}", 1)
    
    # Zone Signature
    pdf.ln(20)
    pdf.set_font("Arial", "I", 10)
    pdf.cell(95, 40, "Signature du Collaborateur :", 1, 0)
    pdf.cell(95, 40, "Validation Manager :", 1, 1)
    
    return pdf.output(dest='S').encode('latin-1')

# --- GESTION DONNÉES ---
def init_db():
    if not os.path.exists(DATA_DIR): os.makedirs(DATA_DIR)
    
    # Colonnes étendues
    cols = ["username","password","role","full_name","department","cp_balance","job_title","base_salary","start_date","rib","address","dob","family_status","phone","contract_type","is_active"]
    if not os.path.exists(USERS_FILE):
        df = pd.DataFrame(columns=cols)
        # Admin par défaut
        df.loc[0] = ["admin","admin123","admin","Admin RH","RH",0,"DRH",0,"2020-01-01","000","Casa","1980-01-01","Célibataire","0600000000","CDI",True]
        df.to_csv(USERS_FILE, index=False)

    if not os.path.exists(REQUESTS_FILE):
        pd.DataFrame(columns=["id", "username", "type", "date_request", "start_date", "end_date", "status", "details"]).to_csv(REQUESTS_FILE, index=False)

def load_data(file_path):
    try: return pd.read_csv(file_path)
    except: init_db(); return pd.read_csv(file_path)

def save_data(df, file_path): df.to_csv(file_path, index=False)

def login(u, p):
    df = load_data(USERS_FILE)
    user = df[(df['username'] == u) & (df['password'] == p) & (df['is_active'] == True)]
    return user.iloc[0] if not user.empty else None

# --- INTERFACES ---

def sidebar_menu(role):
    with st.sidebar:
        st.title("🟣 Yassir RH")
        st.caption(f"Connecté: {st.session_state.user['full_name']}")
        
        if role == 'admin':
            menu = st.radio("Menu Admin", ["Gestion Profils", "Documents RH", "Suivi Planning"])
        else:
            menu = st.radio("Menu Collaborateur", ["Mes Documents", "Mon Planning", "Mes Infos"])
            
        if st.button("Déconnexion"):
            st.session_state.user = None
            st.rerun()
    return menu

# --- PAGE ADMIN ---
def page_admin_profils():
    st.header("👥 Gestion des Profils & Contrats")
    users = load_data(USERS_FILE)
    
    tab1, tab2 = st.tabs(["Ajouter un Collaborateur", "Modifier / Départ"])
    
    with tab1:
        with st.form("new_user"):
            st.subheader("Informations Personnelles")
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
            
            st.subheader("Informations Contractuelles")
            c1, c2, c3 = st.columns(3)
            nu_dept = c1.selectbox("Département", ["IT", "Ops", "Finance", "Marketing"])
            nu_job = c2.text_input("Poste")
            nu_type = c3.selectbox("Type Contrat", ["CDI", "CDD", "Anapec", "Stage"])
            
            c1, c2 = st.columns(2)
            nu_sal = c1.number_input("Salaire Base (MAD)", 5000)
            nu_start = c2.date_input("Date Début")
            
            if st.form_submit_button("✅ Créer le profil"):
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
                st.success("Collaborateur ajouté avec succès !")
                st.rerun()
                
    with tab2:
        st.dataframe(users[users['is_active']==True])
        user_to_edit = st.selectbox("Sélectionner un collaborateur", users[users['role']!='admin']['username'].unique())
        if user_to_edit:
            col_act1, col_act2 = st.columns(2)
            if col_act1.button("⚠️ Marquer comme Démissionnaire / Sortie"):
                users.loc[users['username'] == user_to_edit, 'is_active'] = False
                save_data(users, USERS_FILE)
                st.warning(f"Le profil {user_to_edit} a été désactivé.")
                st.rerun()

def page_doc_generation(is_admin=False):
    st.header("📄 Générateur de Documents Officiels")
    users = load_data(USERS_FILE)
    
    target_user = st.session_state.user
    
    if is_admin:
        st.info("Mode Admin : Générer un document pour un collaborateur")
        choice = st.selectbox("Choisir le collaborateur", users['username'].tolist())
        target_user = users[users['username'] == choice].iloc[0]
    
    st.write(f"**Génération pour : {target_user['full_name']}**")
    
    doc_type = st.selectbox("Type de document", ["Attestation de Travail", "Attestation de Salaire", "Attestation de Congés"])
    
    if st.button("Générer PDF"):
        pdf_bytes = create_pdf_doc(target_user, doc_type)
        st.success("Document généré !")
        st.download_button(
            label="📥 Télécharger le PDF",
            data=pdf_bytes,
            file_name=f"{doc_type}_{target_user['username']}.pdf",
            mime='application/pdf'
        )

def page_planning_timesheet(is_admin=False):
    st.header("🗓️ Planning & Timesheet")
    
    # Simulation simple d'entrée de temps (pour le MVP)
    users = load_data(USERS_FILE)
    target_user = st.session_state.user
    
    if is_admin:
        choice = st.selectbox("Collaborateur", users['username'].tolist(), key="plan_user")
        target_user = users[users['username'] == choice].iloc[0]

    st.subheader(f"Feuille de temps : {target_user['full_name']}")
    
    with st.form("timesheet"):
        col1, col2 = st.columns(2)
        week_start = col1.date_input("Lundi de la semaine")
        hours = col2.number_input("Heures effectuées cette semaine", min_value=0, max_value=80, value=40)
        absences_txt = st.text_area("Déclaration Absences / Remarques", placeholder="Ex: Maladie mardi matin...")
        
        submitted = st.form_submit_button("Générer Feuille de Temps (PDF)")
        
        if submitted:
            pdf_bytes = create_timesheet_pdf(target_user, week_start, hours, absences_txt)
            if hours < 40:
                st.warning(f"⚠️ Attention : 40h non atteintes ({hours}h)")
            else:
                st.success(f"✅ Objectif atteint ({hours}h)")
                
            st.download_button(
                label="📥 Télécharger la Feuille de Temps à Signer",
                data=pdf_bytes,
                file_name=f"Timesheet_{target_user['username']}_{week_start}.pdf",
                mime='application/pdf'
            )

# --- ROUTAGE ---
init_db()

if 'user' not in st.session_state: st.session_state.user = None

if st.session_state.user is None:
    st.markdown("<h1 style='color:#6c1ddb; text-align:center;'>Yassir People</h1>", unsafe_allow_html=True)
    c
