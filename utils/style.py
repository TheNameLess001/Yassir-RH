# utils/style.py
import streamlit as st

YASSIR_PURPLE = "#6200EE" 
BG_COLOR = "#F4F6F9"

def load_css():
    st.markdown(f"""
        <style>
        .stApp {{ background-color: {BG_COLOR}; font-family: 'Segoe UI', sans-serif; }}
        #MainMenu, footer, header {{ visibility: hidden; }}
        .block-container {{ padding-top: 0rem; padding-left: 5rem; padding-right: 1rem; max-width: 100%; }}

        /* NAVBAR & SIDEBAR (Reste en HTML pour le look) */
        .top-navbar {{
            background-color: {YASSIR_PURPLE}; height: 60px; width: 100%; position: fixed; top: 0; left: 0; z-index: 999;
            display: flex; align-items: center; justify-content: space-between; padding: 0 20px; color: white;
        }}
        .custom-sidebar {{
            background-color: white; width: 60px; height: 100vh; position: fixed; top: 60px; left: 0;
            display: flex; flex-direction: column; align-items: center; padding-top: 20px; border-right: 1px solid #e0e0e0; z-index: 998;
        }}
        
        /* STYLE DES VRAIS BOUTONS STREAMLIT POUR QU'ILS RESSEMBLENT AU DESIGN */
        div.stButton > button {{
            width: 100%;
            text-align: left;
            background-color: #f8f9fa;
            border: none;
            color: #555;
            padding: 10px 15px;
            margin-bottom: 5px;
            border-radius: 5px;
            transition: 0.2s;
        }}
        div.stButton > button:hover {{
            background-color: #eef;
            color: {YASSIR_PURPLE};
            border: 1px solid {YASSIR_PURPLE};
        }}
        
        /* CARTE CONTENEUR */
        .css-card {{
            background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            margin-bottom: 20px; border: 1px solid #eaeaea;
        }}
        
        /* PROFIL CERCLE */
        .profile-circle {{
            width: 80px; height: 80px; margin: 0 auto; border-radius: 50%; background: {YASSIR_PURPLE};
            color: white; display: flex; align-items: center; justify-content: center; font-size: 24px;
            border: 3px solid white; box-shadow: 0 0 0 2px {YASSIR_PURPLE};
        }}

        /* ONGLETS (TABS) PERSONNALISÉS */
        .stTabs [data-baseweb="tab-list"] {{ gap: 20px; }}
        .stTabs [data-baseweb="tab"] {{ height: 50px; white-space: pre-wrap; background-color: white; border-radius: 4px; color: #666; }}
        .stTabs [aria-selected="true"] {{ color: {YASSIR_PURPLE} !important; border-bottom-color: {YASSIR_PURPLE} !important; }}
        </style>
    """, unsafe_allow_html=True)

def display_navbar():
    st.markdown(f"""
    <div class="top-navbar">
        <div style="font-weight: bold; font-size: 20px; display: flex; align-items: center; gap: 10px;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="white"><path d="M12 2L2 19h20L12 2zm0 3l6 14H6l6-14z"/></svg> 
            YASSIR <span style="font-weight:normal; font-size:14px; opacity:0.8;">| RH PORTAL</span>
        </div>
        <div style="color:white; opacity:0.8; font-size:14px;">Barre de recherche...</div>
        <div style="display: flex; align-items: center; gap: 15px; font-size: 14px;">
            <div style="background:rgba(255,255,255,0.2); width:35px; height:35px; border-radius:50%; display:flex; align-items:center; justify-content:center;">SB</div>
        </div>
    </div>
    <div class="custom-sidebar">
        <div style="font-size:24px; margin-bottom:20px; cursor:pointer;">🏠</div>
        <div style="font-size:24px; margin-bottom:20px; cursor:pointer;">👤</div>
        <div style="font-size:24px; margin-bottom:20px; cursor:pointer;">📅</div>
    </div>
    """, unsafe_allow_html=True)
