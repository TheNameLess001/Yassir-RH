import streamlit as st
from utils import style

# Configuration
st.set_page_config(page_title="Yassir HR", layout="wide", initial_sidebar_state="collapsed")

# 1. Charger le style et la navbar
style.load_css()
style.display_navbar()

# 2. Header "Bonsoir"
col_head_1, col_head_2 = st.columns([3, 1])
col_head_1.markdown("### Bonsoir SAIF-EDDINE 👋")
col_head_2.markdown('<div style="text-align:right;"><a href="#" class="btn-yassir">+ Nouvelle demande</a></div>', unsafe_allow_html=True)

# 3. La Grille Principale (Layout 1 - 2.2 - 1)
c1, c2, c3 = st.columns([1, 2.2, 1])

# --- COLONNE GAUCHE (PROFIL) ---
with c1:
    st.markdown("""
    <div class="card">
        <div class="profile-img">SB</div>
        <div style="text-align:center; font-weight:bold; margin-top:10px;">SAIF-EDDINE BOUNOIR</div>
        <div style="text-align:center; color:#777; font-size:12px; margin-bottom:15px;">Responsable commercial</div>
        <hr style="border-top:1px solid #eee;">
        <div style="display:flex; justify-content:space-around; font-size:11px; color:#888; margin-bottom:20px;">
            <span>📍 CASABLANCA</span><span>📅 22 Aug 2024</span>
        </div>
        <div class="grid-btn">👤 Profil</div>
        <div class="grid-btn">📅 Calendrier</div>
        <div class="grid-btn">🕒 Tâches</div>
        <div class="grid-btn">📄 Documents</div>
    </div>
    <div class="card"><b>👥 Mon équipe</b><br><span style="color:#aaa; font-size:12px;">Chargement...</span></div>
    """, unsafe_allow_html=True)

# --- COLONNE CENTRALE (DASHBOARD) ---
with c2:
    st.markdown(f"""
    <div class="card" style="min-height: 300px;">
        <div style="font-weight:bold; margin-bottom:15px; border-bottom: 2px solid #f0f0f0; padding-bottom:10px;">
            <span class="tab-item active" style="margin-right:20px;">📅 Absences</span>
            <span class="tab-item" style="margin-right:20px;">📝 Formulaires</span>
            <span class="tab-item">📄 Documents</span>
        </div>
        <div style="text-align:center; padding: 40px; color:#ccc;">
            <div style="font-size:40px;">⚪</div>
            <p>Aucune demande</p>
        </div>
    </div>
    
    <div class="card">
        <div style="display:flex; gap:10px;">
             <div style="background:#eee; height:40px; width:40px; border-radius:50%;"></div>
             <div style="background:#eee; height:15px; width:150px; margin-top:12px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- COLONNE DROITE (ANNONCES) ---
with c3:
    st.markdown("""
    <div class="card" style="height: 350px;">
        <b>📢 Annonces</b>
        <hr style="border-top:1px solid #eee;">
        <div style="text-align:center; padding-top:60px; color:#aaa;">
            <div style="font-size:40px;">📁</div>
            Aucune annonce
        </div>
    </div>
    """, unsafe_allow_html=True)
