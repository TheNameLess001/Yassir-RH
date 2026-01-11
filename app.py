import streamlit as st
import pandas as pd
import os
from datetime import datetime, date, timedelta
from fpdf import FPDF
import base64

# --- CONFIGURATION & CSS ---
st.set_page_config(page_title="Yassir RH Portal", layout="wide", page_icon="🟣")

# CSS pour le Branding Yassir (Sidebar Violette + Titres)
st.markdown("""
    <style>
        /* Couleur de fond de la sidebar */
        [data-testid="stSidebar"] {
            background-color: #6c1ddb;
        }
        /* Texte blanc dans la sidebar */
        [data-testid="stSidebar"] * {
            color: white !important;
        }
        /* Style des expanders dans la sidebar */
        [data-testid="stSidebar"] .streamlit-expanderHeader {
            background-color: #5a18b9;
            color: white;
            border-radius: 5px;
        }
        /* Logo en haut à droite (simulation) */
        .top-right-logo {
            position: absolute;
            top: -50px;
            right: 0px;
            width: 150px;
        }
    </style>
""", unsafe_allow_html=True)

# --- CONSTANTES ---
DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.csv")
PLANNING_FILE = os.path.join(DATA_DIR, "planning.csv")
LOGO_FILE = "logo.png"

# Mentions légales Yassir (Exemple fictif à adapter)
LEGAL_FOOTER = "YASSIR MAROC S.A.R.L | Siège Social : Casanearshore Park, Sidi Maarouf, Casablanca | ICE : 001234567890000 | RC : 123456 | CNSS : 9876543 | Capital Social : 100.000 DHS"

# --- GENERATEUR PDF PROFESSIONNEL ---
class CorporatePDF(FPDF):
    def header(self):
        # Logo centré en haut ou à gauche (Standard pro : Gauche)
        if os.path.exists(LOGO_FILE):
            self.image(LOGO_FILE, 10, 10, 35)
        else:
            self.set_font('Arial', 'B', 20)
            self.set_text_color(108, 29, 219) # Violet Yassir
            self.text(10, 20, "YASSIR")
            
        # Date à droite
        self.set_font('Arial', '', 10)
        self.set_text_color(0, 0, 0)
        self.set_xy(150, 15)
        self.cell(50, 10, f"Casablanca, le {datetime.now().strftime('%d/%m/%Y')}", 0, 0, 'R')
        self.ln(30) # Saut de ligne après en-tête

    def footer(self):
        self.set_y(-20)
        # Ligne de séparation
        self.set_draw_color(200, 200, 200)
        self.line(10, 280, 200, 280)
        # Texte légal
        self.set_font('Arial', '', 7)
        self.set_text_color(100, 100, 100)
        self.multi_cell(0, 4, LEGAL_FOOTER, 0, 'C')

def create_standard_doc(user, doc_type):
    pdf = CorporatePDF()
    pdf.add_page()
    
    # Titre
    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(0, 0, 0) # Noir
    pdf.cell(0, 15, doc_type.upper(), 0, 1, 'C')
    pdf.ln(10)
    
    # Corps
    pdf.set_font("Arial", size=11)
    
    if doc_type == "Attestation de Travail":
        text = f"""Nous soussignés, Société YASSIR MAROC, certifions que :

M./Mme {user['full_name']}
Matricule : {user['username']}
Immatriculé(e) à la CNSS sous le n° : 123456789

Est employé(e) au sein de notre société en qualité de {user['job_title']}.
Date d'entrée : {user['start_date']}
Type de contrat : {user['contract_type']}

Cette attestation est délivrée à l'intéressé(e) pour servir et valoir ce que de droit."""
    
    elif doc_type == "Attestation de Salaire":
        text = f"""Nous certifions que M./Mme {user['full_name']} perçoit à ce jour la rémunération brute mensuelle suivante :

- Salaire de Base : {user['base_salary']} MAD
- Primes fixes : 0.00 MAD
- Indémnités de transport : 500.00 MAD

Soit un Brut Global de : {float(user['base_salary']) + 500} MAD.

Cette attestation est délivrée sur demande de l'intéressé(e)."""

    pdf.multi_cell(0, 8, text)
    
    # Signature
    pdf.ln(30)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(110)
    pdf.cell(0, 10, "La Direction des Ressources Humaines", 0, 1)
    
    return pdf.output(dest='S').encode('latin-1', 'replace')

def create_payslip(user, period):
    pdf = CorporatePDF()
    pdf.add_page()
    
    # En-tête Bulletin
    pdf.set_fill_color(240, 240, 240)
    pdf.rect(10, 40, 190, 25, 'F')
    pdf.set_xy(10, 45)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"BULLETIN DE PAIE - Période : {period}", 0, 1, 'C')
    
    pdf.set_font("Arial", "", 10)
    pdf.ln(5)
    
    # Infos Salarié
    col1_x = 10; col2_x = 110
    curr_y = pdf.get_y()
    
    pdf.text(col1_x, curr_y, f"Nom : {user['full_name']}")
    pdf.text(col2_x, curr_y, f"Fonction : {user['job_title']}")
    pdf.text(col1_x, curr_y+6, f"Matricule : {user['username']}")
    pdf.text(col2_x, curr_y+6, f"Département : {user['department']}")
    pdf.ln(15)
    
    # Tableau Paie
    pdf.set_font("Arial", "B", 10)
    pdf.set_fill_color(108, 29, 219) # Violet Yassir pour l'entête tableau
    pdf.set_text_color(255, 255, 255)
    
    pdf.cell(95, 8, "RUBRIQUES (GAINS)", 1, 0, 'C', 1)
    pdf.cell(30, 8, "BASE", 1, 0, 'C', 1)
    pdf.cell(30, 8, "TAUX", 1, 0, 'C', 1)
    pdf.cell(35, 8, "MONTANT", 1, 1, 'C', 1)
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "", 10)
    
    salary = float(user['base_salary'])
    # Lignes (Simulation simple)
    items = [
        ("Salaire de Base", salary, "-", salary),
        ("Indemnité Transport", 500, "-", 500),
        ("Prime Ancienneté", 0, "-", 0),
        ("RETENUE CNSS", salary, "4.48%", -salary*0.0448),
        ("RETENUE AMO", salary, "2.26%", -salary*0.0226),
        ("RETENUE IGR", salary*0.9, "Barème", -salary*0.10) # Simulée
    ]
    
    total_net = 0
    for name, base, rate, amount in items:
        pdf.cell(95, 8, name, 1)
        pdf.cell(30, 8, str(base), 1, 0, 'R')
        pdf.cell(30, 8, str(rate), 1, 0, 'C')
        pdf.cell(35, 8, f"{amount:.2f}", 1, 1, 'R')
        total_net += amount
        
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(155, 10, "NET A PAYER (MAD)", 1, 0, 'R')
    pdf.set_text_color(108, 29, 219)
    pdf.cell(35, 10, f"{total_net:.2f}", 1, 1, 'C')
    
    return pdf.output(dest='S').encode('latin-1', 'replace')

def create_stc(user):
    pdf = CorporatePDF()
    pdf.add_page()
    
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 15, "SOLDE DE TOUT COMPTE (STC)", 0, 1, 'C')
    pdf.ln(10)
    
    pdf.set_font("Arial", "", 11)
    text = f"""Je soussigné(e), {user['full_name']},

Reconnais avoir reçu de la société YASSIR MAROC, la somme de :
(Montant calculé ci-dessous)
Pour solde de tout compte, suite à la rupture de mon contrat de travail."""
    pdf.multi_cell(0, 7, text)
    
    pdf.ln(10)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, "Détail du calcul :", 0, 1)
    
    pdf.set_font("Arial", "", 11)
    salaire = float(user['base_salary'])
    cp_days = float(user['cp_balance'])
    taux_jour = salaire / 26
    indemnite_cp = cp_days * taux_jour
    salaire_mois_courant = salaire # Suppose mois complet pour l'exemple
    total = indemnite_cp + salaire_mois_courant
    
    pdf.cell(140, 8, f"Salaire du mois en cours :", 1)
    pdf.cell(50, 8, f"{salaire_mois_courant:.2f} MAD", 1, 1, 'R')
    
    pdf.cell(140, 8, f"Indemnité Compensatrice de Congés Payés ({cp_days} jours) :", 1)
    pdf.cell(50, 8, f"{indemnite_cp:.2f} MAD", 1, 1, 'R')
    
    pdf.set_font("Arial", "B", 11)
    pdf.cell(140, 8, "TOTAL NET :", 1)
    pdf.cell(50, 8, f"{total:.2f} MAD", 1, 1, 'R')
    
    pdf.ln(20)
    pdf.cell(0, 10, "Fait à Casablanca, pour servir et valoir décharge définitive.", 0, 1)
    pdf.ln(15)
    pdf.cell(95, 10, "Signature Employeur", 0, 0)
    pdf.cell(95, 10, "Signature Salarié(e) (Précédé de 'Bon pour acquit')", 0, 1)
    
    return pdf.output(dest='S').encode('latin-1', 'replace')

# --- DB & UTILS ---
def init_db():
    if not os.path.exists(DATA_DIR): os.makedirs(DATA_DIR)
    cols = ["username","password","role","full_name","department","cp_balance","job_title","base_salary","start_date","rib","address","dob","family_status","phone","contract_type","is_active"]
    if not os.path.exists(USERS_FILE):
        df = pd.DataFrame(columns=cols)
        df.loc[0] = ["admin","admin123","admin","Admin RH","RH",0,"DRH",0,"2020-01-01","000","Casa","1980-01-01","Célibataire","0600000000","CDI",True]
        df.to_csv(USERS_FILE, index=False)
        
    if not os.path.exists(PLANNING_FILE):
        pd.DataFrame(columns=["username", "date", "status", "start_time", "end_time", "break_min"]).to_csv(PLANNING_FILE, index=False)

def load_data(f): 
    try: return pd.read_csv(f) 
    except: init_db(); return pd.read_csv(f)

def login(u, p):
    df = load_data(USERS_FILE)
    usr = df[(df['username']==u) & (df['password']==p) & (df['is_active']==True)]
    return usr.iloc[0] if not usr.empty else None

# --- UI PAGES ---

def ui_header_logo():
    # Header interface avec Logo à droite
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"## Bienvenue, {st.session_state.user['full_name']}")
        st.caption(f"{st.session_state.user['job_title']} | {st.session_state.user['department']}")
    with col2:
        if os.path.exists(LOGO_FILE):
            st.image(LOGO_FILE, width=120)
        else:
            st.write("**YASSIR**")

def page_mes_documents(user):
    st.subheader("📄 Mes Documents & Bulletins")
    
    tab1, tab2 = st.tabs(["Demande Documents", "Bulletins de Paie"])
    
    with tab1:
        st.info("Les documents sont générés instantanément avec signature électronique.")
        doc_type = st.selectbox("Type de document", ["Attestation de Travail", "Attestation de Salaire"])
        if st.button("Générer & Télécharger"):
            pdf = create_standard_doc(user, doc_type)
            st.download_button("📥 Télécharger PDF", pdf, f"{doc_type}.pdf", "application/pdf")
            
    with tab2:
        period = st.date_input("Période concernée", date.today())
        month_str = period.strftime("%B %Y")
        if st.button(f"Voir Bulletin {month_str}"):
            pdf = create_payslip(user, month_str)
            st.download_button("📥 Télécharger Bulletin", pdf, f"Bulletin_{month_str}.pdf", "application/pdf")

def page_admin_documents():
    st.subheader("🖨️ Édition Documents RH")
    users = load_data(USERS_FILE)
    # Filtre users actifs
    active_users = users[users['is_active'] != False]
    
    selected_u = st.selectbox("Sélectionner Collaborateur", active_users['username'].tolist())
    target = active_users[active_users['username'] == selected_u].iloc[0]
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Documents Standards")
        doc = st.selectbox("Type", ["Attestation de Travail", "Attestation de Salaire"])
        if st.button("Générer Standard"):
            st.download_button("Télécharger", create_standard_doc(target, doc), "doc.pdf", "application/pdf")
            
    with col2:
        st.markdown("#### Sortie / Paie")
        if st.button("⚠️ Générer STC (Solde Tout Compte)"):
            st.download_button("Télécharger STC", create_stc(target), f"STC_{target['username']}.pdf", "application/pdf")
            
        if st.button("Générer Bulletin Mois en cours"):
            st.download_button("Télécharger Bulletin", create_payslip(target, datetime.now().strftime("%B %Y")), "paie.pdf", "application/pdf")

def page_planning_view(role):
    st.subheader("🗓️ Gestion du Temps")
    # (Code simplifié pour la demo, reprenant la logique précédente)
    st.write("Module de planification interactif (voir code précédent pour logique complète)")
    st.info("Utilisez le menu 'Suivi Absences' pour déclarer les congés.")

# --- MAIN APP ---
init_db()

if 'user' not in st.session_state: st.session_state.user = None

if st.session_state.user is None:
    # Login Page stylisée
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if os.path.exists(LOGO_FILE): st.image(LOGO_FILE, width=150)
        st.markdown("<h1 style='color:#6c1ddb;'>Yassir People</h1>", unsafe_allow_html=True)
        u = st.text_input("Identifiant")
        p = st.text_input("Mot de passe", type="password")
        if st.button("Se connecter", type="primary"):
            usr = login(u, p)
            if usr is not None:
                st.session_state.user = usr
                st.rerun()
            else: st.error("Login incorrect")

else:
    # --- INTERFACE CONNECTÉE ---
    user = st.session_state.user
    role = user['role']
    
    # 1. Header Global (Logo droite)
    ui_header_logo()
    st.markdown("---")

    # 2. Sidebar "Menu Glissant" (Accordéons)
    with st.sidebar:
        if os.path.exists(LOGO_FILE): st.image(LOGO_FILE, width=100)
        st.title("Navigation")
        
        selection = None
        
        if role == 'admin':
            with st.expander("👥 Gestion Personnel", expanded=True):
                if st.button("Annuaire / Profils"): selection = "admin_profils"
                if st.button("Contrats & Avenants"): selection = "admin_contrats"
            
            with st.expander("📂 Administration RH"):
                if st.button("Édition Documents"): selection = "admin_docs"
                if st.button("Gestion Paie"): selection = "admin_paie"
            
            with st.expander("🗓️ Temps & Activité"):
                if st.button("Planning Équipe"): selection = "admin_planning"
                if st.button("Validation Congés"): selection = "admin_conges"
                
        else: # Collaborateur
            with st.expander("🏠 Mon Espace", expanded=True):
                if st.button("Mon Profil"): selection = "user_profil"
                if st.button("Mes Objectifs"): selection = "user_obj"
                
            with st.expander("📄 Mes Demandes"):
                if st.button("Documents & Paie"): selection = "user_docs"
                if st.button("Congés & Absences"): selection = "user_abs"
                if st.button("Planning"): selection = "user_plan"

        st.markdown("---")
        if st.button("Déconnexion"):
            st.session_state.user = None
            st.rerun()

    # 3. Routing des pages
    # Note: Streamlit recharge le script à chaque clic, donc on utilise session_state pour mémoriser la page active si besoin,
    # ou on simplifie ici par défaut. Pour un menu bouton, il faut stocker l'état.
    
    if 'current_page' not in st.session_state: st.session_state.current_page = "default"
    if selection: st.session_state.current_page = selection
    
    page = st.session_state.current_page
    
    if page == "user_docs":
        page_mes_documents(user)
    elif page == "admin_docs":
        page_admin_documents()
    elif page == "default":
        st.info("👈 Sélectionnez une option dans le menu à gauche.")
    else:
        st.write(f"Module **{page}** en cours de construction...")
