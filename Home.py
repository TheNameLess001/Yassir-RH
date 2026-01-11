import streamlit as st
import sys
import os

# --- CORRECTION DU CHEMIN (INDISPENSABLE) ---
# Ajoute le dossier courant au chemin de Python pour qu'il trouve le dossier 'utils'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Maintenant on peut importer le style
from utils import style

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Yassir HR Portal",
    layout="wide",
    initial_sidebar_state="collapsed" # On cache la sidebar native Streamlit
)

# --- CHARGEMENT DU DESIGN GLOBAL ---
style.load_css()       # Injecte le CSS (Violet Yassir, Cards, Font)
style.display_navbar() # Affiche la Navbar violette et la Sidebar icônes

# --- ESPACE POUR LA NAVBAR FIXE ---
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# --- CONTENU PRINCIPAL ---

# 1. En-tête (Salutation + Bouton Action)
col_head_1, col_head_2 = st.columns([3, 1])
with col_head_1:
    st.markdown("### Bonsoir SAIF-EDDINE 👋")
with col_head_2:
    # Bouton avec la classe CSS 'btn-yassir' définie dans style.py
    st.markdown('<div style="text-align:right;"><a href="#" class="btn-yassir">+ Nouvelle demande</a></div>', unsafe_allow_html=True)

# 2. Grille de mise en page (3 Colonnes : Profil | Dashboard | Annonces)
c1, c2, c3 = st.columns([1, 2.2, 1])

# --- COLONNE 1 : PROFIL (GAUCHE) ---
with c1:
    st.markdown("""
    <div class="card">
        <div class="profile-img">SB</div>
        
        <div style="text-align:center; font-weight:bold; margin-top:10px; font-size:16px;">SAIF-EDDINE BOUNOIR</div>
        <div style="text-align:center; color:#777; font-size:13px; margin-bottom:15px;">
            Responsable commercial<br>
            <span style="color:#aaa; font-size:12px;">Opérationnel - Racine</span>
        </div>
        
        <hr style="border:0; border-top:1px solid #eee; margin: 15px 0;">
        
        <div style="display:flex; justify-content:space-between; font-size:11px; color:#888; margin-bottom:20px; padding: 0 10px;">
            <span>📍 CASABLANCA</span>
            <span>📅 22 Aug 2024</span>
        </div>
        
        <div class="grid-btn">👤 Profil</div>
        <div class="grid-btn">📅 Calendrier</div>
        <div class="grid-btn">🕒 Tâches</div>
        <div class="grid-btn">📄 Documents</div>
    </div>
    
    <div class="card" style="padding: 15px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <b>👥 Mon équipe</b>
            <span style="color:#ccc;">⋮</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- COLONNE 2 : CENTRE (Suivi des demandes) ---
with c2:
    st.markdown("""
    <div class="card" style="min-height: 350px;">
        <div style="font-weight:bold; margin-bottom:20px;">Suivi des demandes</div>
        
        <div style="border-bottom: 2px solid #f0f0f0; margin-bottom:30px; display:flex; gap:20px; font-size:14px;">
            <div class="tab-item active">📅 Absences <span class="nav-badge" style="background:#eee; color:#666;">0</span></div>
            <div class="tab-item">📝 Formulaires <span class="nav-badge" style="background:#eee; color:#666;">0</span></div>
            <div class="tab-item">📄 Documents <span class="nav-badge" style="background:#eee; color:#666;">0</span></div>
            <div class="tab-item">💸 Note de frais <span class="nav-badge" style="background:#eee; color:#666;">0</span></div>
        </div>
        
        <div style="text-align:center; padding: 30px; color:#ccc;">
            <div style="font-size:40px; margin-bottom:10px; opacity:0.5;">◯</div>
            <div style="height:8px; width:80px; background:#f0f0f0; margin: 0 auto 8px auto; border-radius:4px;"></div>
            <div style="height:8px; width:120px; background:#f0f0f0; margin: 0 auto; border-radius:4px;"></div>
            <p style="margin-top:20px; font-size:13px; color:#999;">Aucune demande</p>
        </div>
    </div>
    
    <div class="card">
        <div style="display:flex; gap:15px; margin-bottom:15px;">
            <div style="background:#f0f0f0; height:40px; width:40px; border-radius:50%;"></div>
            <div style="background:#f0f0f0; height:15px; width:200px; border-radius:4px; margin-top:12px;"></div>
        </div>
        <div style="display:flex; gap:10px;">
            <div style="background:#f4f6f9; height:80px; flex:1; border-radius:6px;"></div>
            <div style="background:#f4f6f9; height:80px; flex:1; border-radius:6px;"></div>
            <div style="background:#f4f6f9; height:80px; flex:1; border-radius:6px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- COLONNE 3 : DROITE (Annonces) ---
with c3:
    st.markdown("""
    <div class="card" style="height: 380px;">
        <div style="font-weight:bold; margin-bottom:10px;">📢 Annonces</div>
        <hr style="border:0; border-top:1px solid #eee; margin-bottom:20px;">
        
        <div style="text-align:center; padding-top:80px; color:#aaa;">
            <div style="font-size:48px; margin-bottom:10px; opacity:0.3;">📁</div>
            <div style="font-size:13px;">Aucune annonce à afficher</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
