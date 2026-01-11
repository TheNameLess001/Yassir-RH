import streamlit as st
import pandas as pd
import os
from datetime import datetime
from fpdf import FPDF

# --- CONSTANTES ---
DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.csv")
PLANNING_FILE = os.path.join(DATA_DIR, "planning.csv")
LOGO_FILE = "logo.png"

# INFOS JURIDIQUES YASSIR (A modifier avec les vraies infos)
COMPANY_INFO = {
    "name": "YASSIR MAROC S.A.R.L",
    "address": "Casanearshore Park, Sidi Maarouf, 20270 Casablanca",
    "rc": "RC: 345678",
    "ice": "ICE: 001567890000045",
    "cnss": "CNSS: 8765432",
    "patente": "Patente: 34561234",
    "capital": "Capital Social: 100.000 DHS"
}

# --- CSS / STYLE ---
def apply_style():
    st.markdown("""
        <style>
            [data-testid="stSidebar"] { background-color: #6c1ddb; }
            [data-testid="stSidebar"] * { color: white !important; }
            .st-emotion-cache-6qob1r { background-color: rgba(255,255,255,0.1); border-radius: 5px; margin-bottom: 5px; }
            div[data-testid="stSidebarNav"] ul { padding-top: 20px; }
        </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNEES ---
def init_db():
    if not os.path.exists(DATA_DIR): os.makedirs(DATA_DIR)
    
    # On ajoute CIN et CNSS dans les colonnes requises
    cols = ["username","password","role","full_name","department","cp_balance","job_title",
            "base_salary","start_date","rib","address","dob","family_status","phone",
            "contract_type","cin","cnss_number","is_active"]
            
    if not os.path.exists(USERS_FILE):
        df = pd.DataFrame(columns=cols)
        # Admin par défaut
        df.loc[0] = ["admin","admin123","admin","Admin RH","RH",0,"DRH",0,"2020-01-01",
                     "000","Casa","1980-01-01","Célibataire","0600000000","CDI","BH00000","123456789",True]
        df.to_csv(USERS_FILE, index=False)
        
    if not os.path.exists(PLANNING_FILE):
        pd.DataFrame(columns=["username", "date", "status", "start_time", "end_time", "break_min"]).to_csv(PLANNING_FILE, index=False)

def load_data(f):
    try:
        df = pd.read_csv(f)
        # Auto-réparation colonnes manquantes
        if f == USERS_FILE:
            needed = ["cin", "cnss_number", "is_active"]
            save = False
            for col in needed:
                if col not in df.columns:
                    df[col] = "N/A" if col != "is_active" else True
                    save = True
            if save: df.to_csv(f, index=False)
        return df
    except:
        init_db()
        return pd.read_csv(f)

def save_data(df, f): df.to_csv(f, index=False)

def check_auth():
    if 'user' not in st.session_state or st.session_state.user is None:
        st.warning("Veuillez vous connecter.")
        st.stop()

# --- MOTEUR PDF PROFESSIONNEL ---
class YassirPDF(FPDF):
    def header(self):
        # Logo à gauche
        if os.path.exists(LOGO_FILE):
            self.image(LOGO_FILE, 10, 10, 30)
        
        # Infos Entreprise à Droite (Alignées)
        self.set_font('Arial', 'B', 10)
        self.set_text_color(108, 29, 219) # Violet Yassir
        self.set_xy(110, 10)
        self.cell(90, 5, COMPANY_INFO["name"], 0, 1, 'R')
        
        self.set_font('Arial', '', 8)
        self.set_text_color(80, 80, 80) # Gris foncé
        self.set_x(110)
        self.cell(90, 4, COMPANY_INFO["address"], 0, 1, 'R')
        self.set_x(110)
        self.cell(90, 4, f"{COMPANY_INFO['rc']} | {COMPANY_INFO['ice']}", 0, 1, 'R')
        self.set_x(110)
        self.cell(90, 4, f"{COMPANY_INFO['cnss']} | {COMPANY_INFO['patente']}", 0, 1, 'R')
        
        self.ln(20) # Marge après header

    def footer(self):
        self.set_y(-20)
        self.set_draw_color(200, 200, 200)
        self.line(10, 275, 200, 275) # Ligne grise
        self.set_font('Arial', 'I', 7)
        self.set_text_color(128)
        self.cell(0, 5, f"{COMPANY_INFO['name']} - {COMPANY_INFO['address']}", 0, 1, 'C')
        self.cell(0, 4, f"{COMPANY_INFO['rc']} - {COMPANY_INFO['ice']} - {COMPANY_INFO['capital']}", 0, 0, 'C')

# --- FONCTIONS DE GENERATION ---

def safe_str(val):
    """Encode pour éviter erreurs accents FPDF basic"""
    return str(val).encode('latin-1', 'replace').decode('latin-1')

def create_work_certificate(user):
    pdf = YassirPDF()
    pdf.add_page()
    
    # Titre
    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 15, "ATTESTATION DE TRAVAIL", 0, 1, 'C')
    pdf.ln(10)
    
    # Corps
    pdf.set_font("Arial", "", 12)
    text = f"""Nous soussignés, {safe_str(COMPANY_INFO['name'])}, certifions par la présente que :

M./Mme : {safe_str(user['full_name'])}
Matricule : {safe_str(user['username'])}
CIN n° : {safe_str(user.get('cin', ''))}
Immatriculé(e) à la CNSS sous le n° : {safe_str(user.get('cnss_number', ''))}

Est employé(e) au sein de notre société en qualité de : {safe_str(user['job_title'])}
Depuis le : {safe_str(user['start_date'])}
Type de contrat : {safe_str(user['contract_type'])}

Cette attestation est délivrée à l'intéressé(e) pour servir et valoir ce que de droit.
"""
    pdf.multi_cell(0, 8, text)
    
    # Date et Signature
    pdf.ln(20)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Fait à Casablanca, le {datetime.now().strftime('%d/%m/%Y')}", 0, 1, 'R')
    
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(10)
    pdf.cell(0, 10, "Direction des Ressources Humaines", 0, 1, 'L')
    
    return pdf.output(dest='S').encode('latin-1', 'replace')

def create_payslip_pdf(user, month_str):
    pdf = YassirPDF()
    pdf.add_page()
    
    # Titre Bulletin
    pdf.set_fill_color(240, 240, 240)
    pdf.rect(10, 45, 190, 25, 'F')
    
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"BULLETIN DE PAIE", 0, 1, 'C')
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Période : {safe_str(month_str)}", 0, 1, 'C')
    pdf.ln(10)
    
    # Infos Employé (Cadre)
    pdf.set_font("Arial", "", 10)
    y_start = pdf.get_y()
    
    # Gauche
    pdf.text(12, y_start+5, f"Nom Prénom : {safe_str(user['full_name'])}")
    pdf.text(12, y_start+10, f"Matricule : {safe_str(user['username'])}")
    pdf.text(12, y_start+15, f"Fonction : {safe_str(user['job_title'])}")
    
    # Droite
    pdf.text(110, y_start+5, f"CIN : {safe_str(user.get('cin', 'N/A'))}")
    pdf.text(110, y_start+10, f"CNSS : {safe_str(user.get('cnss_number', 'N/A'))}")
    pdf.text(110, y_start+15, f"Entrée le : {safe_str(user['start_date'])}")
    
    pdf.ln(25)
    
    # TABLEAU SALAIRE
    # En-tête Tableau
    pdf.set_fill_color(108, 29, 219) # Violet
    pdf.set_text_color(255, 255, 255) # Blanc
    pdf.set_font("Arial", "B", 10)
    
    pdf.cell(80, 8, "RUBRIQUES", 1, 0, 'C', 1)
    pdf.cell(30, 8, "BASE", 1, 0, 'C', 1)
    pdf.cell(20, 8, "TAUX", 1, 0, 'C', 1)
    pdf.cell(30, 8, "GAINS (+)", 1, 0, 'C', 1)
    pdf.cell(30, 8, "RETENUES (-)", 1, 1, 'C', 1)
    
    # Contenu Tableau
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "", 10)
    
    # Calculs simulés
    salaire_base = float(user['base_salary'])
    transport = 500.00
    brut = salaire_base + transport
    
    cnss = min(brut, 6000) * 0.0448
    amo = brut * 0.0226
    # Simulation IGR très simplifiée
    net_imposable = brut - cnss - amo - (brut * 0.20)
    igr = max(0, net_imposable * 0.10) 
    
    items = [
        ["Salaire de Base", salaire_base, "", salaire_base, ""],
        ["Indemnité Transport", 500.00, "", 500.00, ""],
        ["Retenue CNSS", min(brut,6000), "4.48%", "", f"{cnss:.2f}"],
        ["Retenue AMO", brut, "2.26%", "", f"{amo:.2f}"],
        ["Impôt sur le Revenu (IR)", "", "Barème", "", f"{igr:.2f}"]
    ]
    
    total_gains = salaire_base + transport
    total_retenues = cnss + amo + igr
    net_payer = total_gains - total_retenues
    
    for row in items:
        pdf.cell(80, 8, safe_str(row[0]), 1)
        pdf.cell(30, 8, str(row[1]) if row[1] else "", 1, 0, 'R')
        pdf.cell(20, 8, str(row[2]), 1, 0, 'C')
        pdf.cell(30, 8, str(row[3]) if row[3] else "", 1, 0, 'R')
        pdf.cell(30, 8, str(row[4]) if row[4] else "", 1, 1, 'R')
        
    # Totaux
    pdf.set_font("Arial", "B", 10)
    pdf.cell(130, 8, "TOTAUX", 1, 0, 'R')
    pdf.cell(30, 8, f"{total_gains:.2f}", 1, 0, 'R')
    pdf.cell(30, 8, f"{total_retenues:.2f}", 1, 1, 'R')
    
    pdf.ln(5)
    
    # NET A PAYER
    pdf.set_font("Arial", "B", 14)
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(130, 12, "NET A PAYER (MAD)", 1, 0, 'R', 1)
    pdf.set_text_color(108, 29, 219)
    pdf.cell(60, 12, f"{net_payer:.2f} MAD", 1, 1, 'C', 1)
    
    return pdf.output(dest='S').encode('latin-1', 'replace')
