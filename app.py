import streamlit as st
import pandas as pd
import os
from datetime import datetime, date, timedelta
from fpdf import FPDF

# --- 1. CONFIGURATION & STYLE ---
st.set_page_config(page_title="Yassir RH Portal", layout="wide", page_icon="🟣")

st.markdown("""
    <style>
        /* Fond Violet Yassir pour la Sidebar */
        [data-testid="stSidebar"] {
            background-color: #6c1ddb;
        }
        /* Texte blanc dans la sidebar */
        [data-testid="stSidebar"] * {
            color: white !important;
        }
        /* BOUTONS BLANCS TEXTE VIOLET (Correction Contraste) */
        [data-testid="stSidebar"] button {
            background-color: white !important;
            color: #6c1ddb !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: bold !important;
            margin-bottom: 5px !important;
            width: 100%;
        }
        [data-testid="stSidebar"] button:hover {
            background-color: #f0f0f0 !important;
            color: #5a18b9 !important;
        }
        /* Style des Expanders */
        [data-testid="stSidebar"] .streamlit-expanderHeader {
            background-color: rgba(255, 255, 255, 0.1) !important;
            color: white !important;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# --- CONSTANTES ---
DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.csv")
PLANNING_FILE = os.path.join(DATA_DIR, "planning.csv")
LOGO_FILE = "logo.png"

# --- UTILITAIRES ---
def init_db():
    if not os.path.exists(DATA_DIR): os.makedirs(DATA_DIR)
    
    # Colonnes complètes
    cols = ["username","password","role","full_name","department","cp_balance","job_title","base_salary","start_date","rib","address","dob","family_status","phone","contract_type","is_active"]
    
    if not os.path.exists(USERS_FILE):
        df = pd.DataFrame(columns=cols)
        # Admin par défaut
        df.loc[0] = ["admin","admin123","admin","Admin RH","RH",0,"DRH",0,"2020-01-01","000","Casa","1980-01-01","Célibataire","0600000000","CDI",True]
        df.to_csv(USERS_FILE, index=False)
        
    if not os.path.exists(PLANNING_FILE):
        pd.DataFrame(columns=["username", "date", "status", "start_time", "end_time", "break_min"]).to_csv(PLANNING_FILE, index=False)

def load_data(f): 
    # Fonction AUTO-RÉPARATRICE
    try: 
        df = pd.read_csv(f)
        
        # Correction spécifique pour l'erreur KeyError: 'is_active'
        if f == USERS_FILE:
            # Si des colonnes manquent (vieux fichier), on les ajoute
            required_cols = ["username","password","role","full_name","department","cp_balance","job_title","base_salary","start_date","rib","address","dob","family_status","phone","contract_type","is_active"]
            save_needed = False
            for col in required_cols:
                if col not in df.columns:
                    if col == 'is_active':
                        df[col] = True # Par défaut tout le monde est actif
                    else:
                        df[col] = "" # Vide par défaut
                    save_needed = True
            
            if save_needed:
                df.to_csv(f, index=False)
                
        return df
    except: 
        init_db()
        return pd.read_csv(f)

def save_data(df, f): df.to_csv(f, index=False)

def login(u, p):
    df = load_data(USERS_FILE)
    # Vérification sécurisée
    if 'is_active' in df.columns:
        usr = df[(df['username']==u) & (df['password']==p) & (df['is_active']==True)]
    else:
        # Fallback si jamais la réparation a échoué (rare)
        usr = df[(df['username']==u) & (df['password']==p)]
        
    return usr.iloc[0] if not usr.empty else None

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
        self.cell(0, 10, 'Yassir Maroc - Document Interne', 0, 0, 'C')

def generate_planning_pdf(user_name, week_start, data, total_h):
    pdf = YassirPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"FEUILLE DE TEMPS : {user_name}", 0, 1, 'C')
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Semaine du : {week_start}", 0, 1, 'C')
    pdf.ln(10)
    
    # Tableau simple
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(40, 10, "Date", 1, 0, 'C', 1)
    pdf.cell(40, 10, "Statut", 1, 0, 'C', 1)
    pdf.cell(30, 10, "Heures", 1, 1, 'C', 1)
    
    for item in data:
        pdf.cell(40, 10, str(item['Date']), 1)
        pdf.cell(40, 10, str(item['Statut']), 1)
        pdf.cell(30, 10, str(item['H']), 1, 1)
        
    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"TOTAL: {total_h} Heures", 0, 1, 'R')
    return pdf.output(dest='S').encode('latin-1', 'replace')

# --- PAGES ---

def page_planning_interactif(role):
    st.subheader("🗓️ Planification & Suivi Hebdomadaire")
    
    # 1. Sélecteurs
    c1, c2 = st.columns(2)
    selected_date = c1.date_input("Semaine du", date.today() - timedelta(days=date.today().weekday()))
    monday = selected_date - timedelta(days=selected_date.weekday())
    
    target_user = st.session_state.user['username']
    if role == 'admin':
        users = load_data(USERS_FILE)
        target_name = c2.selectbox("Collaborateur", users['username'].tolist())
        target_user = target_name
    
    st.info(f"Semaine du **{monday.strftime('%d/%m/%Y')}** pour **{target_user}**")
    
    # 2. Préparation Données
    df_plan = load_data(PLANNING_FILE)
    week_days = [monday + timedelta(days=i) for i in range(7)] 
    
    editor_data = []
    for day in week_days:
        d_str = day.strftime("%Y-%m-%d")
        existing = df_plan[(df_plan['username'] == target_user) & (df_plan['date'] == d_str)]
        
        if not existing.empty:
            row = existing.iloc[0]
            editor_data.append({"Date": d_str, "Statut": row['status'], "Début": row['start_time'], "Fin": row['end_time'], "Pause": int(row['break_min'])})
        else:
            is_weekend = day.weekday() >= 5
            editor_data.append({
                "Date": d_str, 
                "Statut": "Repos" if is_weekend else "Travail",
                "Début": "-" if is_weekend else "09:00",
                "Fin": "-" if is_weekend else "18:00",
                "Pause": 0 if is_weekend else 60
            })
            
    # 3. Tableau Interactif
    edited = st.data_editor(
        pd.DataFrame(editor_data),
        column_config={
            "Statut": st.column_config.SelectboxColumn(options=["Travail", "Télétravail", "Congé Payé", "Maladie", "Repos"], required=True),
            "Début": st.column_config.TextColumn(width="small"),
            "Fin": st.column_config.TextColumn(width="small"),
            "Pause": st.column_config.NumberColumn("Pause (min)", min_value=0, max_value=120)
        },
        hide_index=True,
        use_container_width=True,
        key=f"edit_{target_user}_{monday}"
    )
    
    # 4. Calculs & Save
    total_h = 0
    clean_data = []
    for idx, row in edited.iterrows():
        h = 0
        if row['Statut'] in ['Travail', 'Télétravail']:
            h = calculate_hours(row['Début'], row['Fin'], row['Pause'])
        total_h += h
        clean_data.append({"Date": row['Date'], "Statut": row['Statut'], "H": h})
        
    st.metric("Total Heures", f"{total_h}h", delta="Obj: 40h", delta_color="normal" if total_h >= 40 else "inverse")
    
    c1, c2 = st.columns(2)
    if c1.button("💾 Sauvegarder"):
        week_str = [d.strftime("%Y-%m-%d") for d in week_days]
        df_plan = df_plan[~((df_plan['username'] == target_user) & (df_plan['date'].isin(week_str)))]
        new_rows = []
        for index, row in edited.iterrows():
            new_rows.append({
                "username": target_user, "date": row['Date'], "status": row['Statut'],
                "start_time": row['Début'], "end_time": row['Fin'], "break_min": row['Pause']
            })
        save_data(pd.concat([df_plan, pd.DataFrame(new_rows)], ignore_index=True), PLANNING_FILE)
        st.success("Sauvegardé !")
        
    if c2.button("🖨️ PDF"):
        pdf = generate_planning_pdf(target_user, monday.strftime("%d/%m"), clean_data, total_h)
        st.download_button("Télécharger", pdf, "timesheet.pdf", "application/pdf")

def page_profil_user():
    st.header("👤 Mon Profil")
    user = st.session_state.user
    with st.form("my_profile"):
        c1, c2 = st.columns(2)
        new_addr = c1.text_input("Adresse", user.get('address', ''))
        new_phone = c2.text_input("Téléphone", user.get('phone', ''))
        new_pass = c1.text_input("Mot de passe (si changement)", type="password")
        c2.info("Contactez RH pour autres changements.")
        if st.form_submit_button("Mettre à jour"):
            df = load_data(USERS_FILE)
            idx = df[df['username'] == user['username']].index[0]
            df.at[idx, 'address'] = new_addr
            df.at[idx, 'phone'] = new_phone
            if new_pass: df.at[idx, 'password'] = new_pass
            save_data(df, USERS_FILE)
            st.session_state.user = df.iloc[idx]
            st.success("Profil mis à jour !")
            st.rerun()

# --- MAIN ---
init_db()

if 'user' not in st.session_state: st.session_state.user = None

if st.session_state.user is None:
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown("<br><h1 style='color:#6c1ddb; text-align:center;'>Yassir People</h1>", unsafe_allow_html=True)
        u = st.text_input("Identifiant")
        p = st.text_input("Mot de passe", type="password")
        if st.button("Se connecter", type="primary", use_container_width=True):
            usr = login(u, p)
            if usr is not None: 
                st.session_state.user = usr
                st.rerun()
            else: st.error("Erreur d'accès")

else:
    # Header
    c1, c2 = st.columns([4,1])
    with c1: st.title(f"Bonjour, {st.session_state.user['full_name']}")
    with c2: 
        if os.path.exists(LOGO_FILE): st.image(LOGO_FILE, width=120)

    # Sidebar Menu
    with st.sidebar:
        if os.path.exists(LOGO_FILE): st.image(LOGO_FILE, use_container_width=True)
        st.write("")
        
        role = st.session_state.user['role']
        menu_select = None
        
        if role == 'admin':
            with st.expander("👥 Gestion Personnel", expanded=True):
                if st.button("Annuaire / Profils"): menu_select = "admin_users"
                if st.button("Contrats"): menu_select = "admin_contrats"
            with st.expander("📂 Administration RH"):
                if st.button("Documents"): menu_select = "admin_docs"
            with st.expander("🗓️ Temps & Activité"):
                if st.button("Planning Global"): menu_select = "admin_plan"
        else:
            with st.expander("🏠 Mon Espace", expanded=True):
                if st.button("Mon Profil"): menu_select = "user_profil"
                if st.button("Mon Planning"): menu_select = "user_plan"

        st.markdown("---")
        if st.button("Déconnexion"):
            st.session_state.user = None
            st.rerun()

    # Routing
    if 'page' not in st.session_state: st.session_state.page = "default"
    if menu_select: st.session_state.page = menu_select
    pg = st.session_state.page
    
    if pg == "user_profil": page_profil_user()
    elif pg == "user_plan": page_planning_interactif('user')
    elif pg == "admin_plan": page_planning_interactif('admin')
    elif pg == "admin_users": 
        st.subheader("Annuaire")
        st.dataframe(load_data(USERS_FILE))
    elif pg == "default": st.info("Bienvenue sur le portail Yassir RH.")
    else: st.warning("Module en maintenance.")
