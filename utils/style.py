# utils/style.py
import streamlit as st

# --- COULEURS YASSIR (REBRANDING) ---
YASSIR_PURPLE = "#6200EE" 
BG_COLOR = "#F4F6F9"

def load_css():
    """Injecte le CSS global et la structure de la page."""
    st.markdown(f"""
        <style>
        /* FOND ET POLICE */
        .stApp {{
            background-color: {BG_COLOR};
            font-family: 'Segoe UI', sans-serif;
        }}
        
        /* HIDE STREAMLIT DEFAULT ELEMENTS */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        .block-container {{
            padding-top: 0rem;
            padding-left: 5rem; /* Espace pour la sidebar custom */
            padding-right: 1rem;
            max-width: 100%;
        }}

        /* --- NAVBAR DU HAUT (VIOLET) --- */
        .top-navbar {{
            background-color: {YASSIR_PURPLE};
            height: 60px;
            width: 100%;
            position: fixed;
            top: 0;
            left: 0;
            z-index: 999;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 20px;
            color: white;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .search-bar {{
            background: rgba(255,255,255,0.2);
            border: none;
            padding: 8px 15px;
            border-radius: 5px;
            color: white;
            width: 300px;
        }}
        .nav-badge {{
            background-color: #00C853; 
            padding: 2px 8px; 
            border-radius: 12px; 
            font-size: 10px;
        }}

        /* --- SIDEBAR GAUCHE (ICONES) --- */
        .custom-sidebar {{
            background-color: white;
            width: 60px;
            height: 100vh;
            position: fixed;
            top: 60px;
            left: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding-top: 20px;
            border-right: 1px solid #e0e0e0;
            z-index: 998;
        }}
        .sidebar-icon {{
            color: #9aa0ac;
            font-size: 20px;
            margin-bottom: 30px;
            cursor: pointer;
            text-decoration: none;
        }}
        .sidebar-icon:hover {{ color: {YASSIR_PURPLE}; }}

        /* --- CARDS & WIDGETS --- */
        .card {{
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            margin-bottom: 20px;
            border: 1px solid #eaeaea;
        }}
        
        /* PROFIL CERCLE */
        .profile-img {{
            width: 80px; height: 80px;
            border-radius: 50%;
            background-color: {YASSIR_PURPLE};
            color: white;
            display: flex; align-items: center; justify-content: center;
            font-size: 24px;
            border: 3px solid #fff;
            box-shadow: 0 0 0 2px {YASSIR_PURPLE};
            margin: 0 auto;
        }}
        
        /* BOUTONS INTERNES */
        .grid-btn {{
            background-color: #f8f9fa;
            padding: 10px; border-radius: 5px;
            margin-bottom: 8px; font-size: 13px;
            color: #555; cursor: pointer;
        }}
        .grid-btn:hover {{ background-color: #eef; color: {YASSIR_PURPLE}; }}
        
        /* TABS CUSTOM */
        .tab-item.active {{
            color: {YASSIR_PURPLE};
            border-bottom: 2px solid {YASSIR_PURPLE};
        }}
        
        /* BOUTON GLOBAL */
        .btn-yassir {{
            background-color: {YASSIR_PURPLE};
            color: white;
            padding: 8px 16px;
            border-radius: 5px;
            text-decoration: none;
            font-weight: bold;
        }}
        </style>
    """, unsafe_allow_html=True)

def display_navbar():
    """Affiche la barre de navigation et la sidebar HTML."""
    st.markdown("""
    <div class="top-navbar">
        <div style="font-weight: bold; font-size: 20px; display: flex; align-items: center; gap: 10px;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="white"><path d="M12 2L2 19h20L12 2zm0 3l6 14H6l6-14z"/></svg> 
            YASSIR <span style="font-weight:normal; font-size:14px; opacity:0.8;">| RH PORTAL</span>
        </div>
        <input class="search-bar" type="text" placeholder="Rechercher document, collaborateur...">
        <div style="display: flex; align-items: center; gap: 15px; font-size: 14px;">
            <span>Tâches <span class="nav-badge">0</span></span>
            <div style="background:rgba(255,255,255,0.2); width:35px; height:35px; border-radius:50%; display:flex; align-items:center; justify-content:center;">SB</div>
        </div>
    </div>
    
    <div class="custom-sidebar">
        <a href="#" class="sidebar-icon">🏠</a>
        <a href="#" class="sidebar-icon">👤</a>
        <a href="#" class="sidebar-icon">📅</a>
        <a href="#" class="sidebar-icon">📄</a>
    </div>
    
    <div style='height: 80px;'></div> """, unsafe_allow_html=True)
