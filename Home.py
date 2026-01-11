import streamlit as st
import sys
import os

# --- CORRECTION CHEMIN ---
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import style

st.set_page_config(page_title="Yassir HR", layout="wide", initial_sidebar_state="collapsed")

# Chargement style
style.load_css()
style.display_navbar()

# Espace pour navbar fixe
st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)

# --- HEADER ---
c_h1, c_h2 = st.columns([3, 1])
c_h1.markdown("### Bonsoir SAIF-EDDINE 👋")
if c_h2.button("+ Nouvelle demande", type="primary"):
    st.toast("Ouverture du formulaire de demande...") # C'est ici que l'action se passe !

# --- LAYOUT PRINCIPAL ---
c1, c2, c3 = st.columns([1, 2.2, 1])

# === COLONNE 1 : PROFIL (INTERACTIF) ===
with c1:
    # On ouvre un conteneur style "Carte"
    with st.container():
        st.markdown('<div class="css-card">', unsafe_allow_html=True)
        
        # Partie HTML (Image + Info)
        st.markdown("""
            <div class="profile-circle">SB</div>
            <div style="text-align:center; font-weight:bold; margin-top:10px;">SAIF-EDDINE BOUNOIR</div>
            <div style="text-align:center; color:#777; font-size:12px; margin-bottom:15px;">Responsable commercial</div>
            <hr style="border-top:1px solid #eee;">
        """, unsafe_allow_html=True)
        
        # VRAIS BOUTONS INTERACTIFS
        if st.button("👤 Profil"):
            st.write("Navigation vers Profil...")
            # st.switch_page("pages/Profil.py") # Décommentez si vous avez la page
            
        if st.button("📅 Calendrier"):
            st.write("Ouverture calendrier...")
            
        if st.button("🕒 Tâches"):
            st.write("Chargement tâches...")
            
        if st.button("📄 Documents"):
            st.write("Ouverture documents...")

        st.markdown('</div>', unsafe_allow_html=True) # Fin Carte

    # Widget Equipe
    st.markdown("""
    <div class="css-card" style="padding:15px; margin-top:-10px;">
        <b>👥 Mon équipe</b>
    </div>
    """, unsafe_allow_html=True)

# === COLONNE 2 : DASHBOARD (ONGETS ACTIFS) ===
with c2:
    st.markdown('<div class="css-card" style="min-height: 400px;">', unsafe_allow_html=True)
    st.markdown('<div style="font-weight:bold; margin-bottom:10px;">Suivi des demandes</div>', unsafe_allow_html=True)
    
    # VRAIS ONGLETS STREAMLIT
    tab1, tab2, tab3, tab4 = st.tabs(["📅 Absences", "📝 Formulaires", "📄 Documents", "💸 Notes de frais"])
    
    with tab1:
        st.info("Aucune absence récente.")
        # Ici vous pouvez mettre st.dataframe() ou des graphiques
        
    with tab2:
        st.write("Aucun formulaire en attente.")
        
    with tab3:
        st.write("Vos documents sont à jour.")
        
    with tab4:
        st.write("Aucune note de frais.")
        
    st.markdown('</div>', unsafe_allow_html=True)

    # Widget bas (News)
    st.markdown('<div class="css-card">Actualités Yassir...</div>', unsafe_allow_html=True)

# === COLONNE 3 : ANNONCES ===
with c3:
    st.markdown("""
    <div class="css-card" style="height: 400px;">
        <b>📢 Annonces</b>
        <hr style="border-top:1px solid #eee;">
        <div style="text-align:center; padding-top:80px; color:#aaa;">
            <div style="font-size:40px;">📁</div>
            Aucune annonce
        </div>
    </div>
    """, unsafe_allow_html=True)
