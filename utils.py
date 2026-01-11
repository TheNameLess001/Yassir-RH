# utils.py
import streamlit as st
import pandas as pd
import os
from datetime import datetime
from fpdf import FPDF

# --- CONFIGURATION ---
DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.csv")
PLANNING_FILE = os.path.join(DATA_DIR, "planning.csv")
LOGO_FILE = "logo.png"

# --- CSS PARTAGÉ ---
def apply_style():
    # Cache la navigation native automatique pour gérer la sécu nous-mêmes si besoin
    # Mais ici on style juste la sidebar en Violet Yassir
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                background-color: #6c1ddb;
            }
            [data-testid="stSidebar"] * {
                color: white !important;
            }
            /* Style des liens de navigation natifs Streamlit */
            .st-emotion-cache-6qob1r {
                background-color: rgba(255,255,255,0.1);
                border-radius: 5px;
                margin-bottom: 5px;
            }
            div[data-testid="stSidebarNav"] ul {
                padding-top: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

# --- GESTION DONNÉES ---
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
    try:
        df = pd.read_csv(f)
        if f == USERS_FILE and 'is_active' not in df.columns:
            # Auto-repair
            df['is_active'] = True
            df.to_csv(f, index=False)
        return df
    except:
        init_db()
        return pd.read_csv(f)

def save_data(df, f): df.to_csv(f, index=False)

def check_auth():
    """Vérifie si l'utilisateur est connecté, sinon redirige vers Home"""
    if 'user' not in st.session_state or st.session_state.user is None:
        st.warning("Veuillez vous connecter sur la page d'accueil.")
        st.switch_page("Home.py")

# --- CALCUL HEURES ---
def calculate_hours(start, end, pause):
    try:
        if str(start) == "-" or str(end) == "-": return 0.0
        fmt = "%H:%M"
        t1 = datetime.strptime(str(start), fmt)
        t2 = datetime.strptime(str(end), fmt)
        hours = (t2 - t1).total_seconds() / 3600
        return round(max(0.0, hours - (pause/60)), 2)
    except: return 0.0

# --- PDF GENERATOR ---
class YassirPDF(FPDF):
    def header(self):
        if os.path.exists(LOGO_FILE): self.image(LOGO_FILE, 10, 10, 30)
        self.set_font('Arial', 'B', 12)
        self.set_text_color(108, 29, 219)
        self.cell(0, 10, "YASSIR MAROC - RH", 0, 1, 'R')
        self.ln(15)
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Document Interne Yassir', 0, 0, 'C')

def create_pdf(user, type_doc):
    pdf = YassirPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, type_doc.upper(), 0, 1, 'C')
    pdf.ln(20)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, f"Ce document atteste que {user['full_name']} (Matricule {user['username']}) travaille chez Yassir.\n\nPoste: {user['job_title']}\nDépartement: {user['department']}")
    return pdf.output(dest='S').encode('latin-1', 'replace')
