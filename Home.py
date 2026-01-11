import streamlit as st
import os

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Yassir HR Portal",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. INJECTION DU STYLE CSS ET DU HTML FIXE ---
def load_css():
    css_file = os.path.join("assets", "style.css")
    with open(css_file, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Injection de la Navbar et Sidebar en HTML pur (car Streamlit ne permet pas ce layout natif)
    st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <div class="top-navbar">
        <div style="font-weight: bold; font-size: 20px; display: flex; align-items: center; gap: 10px;">
            <i class="fa-solid fa-shapes"></i> YASSIR <span style="font-weight:normal; font-size:14px; opacity:0.8; margin-left:5px;">| RH PORTAL</span>
        </div>
        
        <div class="search-container">
             <input type="text" placeholder="Rechercher document, collaborateur...">
        </div>
        
        <div style="display: flex; align-items: center; gap: 20px; font-size: 14px;">
            <div style="cursor:pointer">Tâches <span class="badge-count">0</span></div>
            <div style="background:#5000c9; width:35px; height:35px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:bold;">SB</div>
        </div>
    </div>
    
    <div class="left-sidebar">
        <a class="sidebar-icon active"><i class="fa-solid fa-house"></i></a>
        <a class="sidebar-icon"><i class="fa-solid fa-user"></i></a>
        <a class="sidebar-icon"><i class="fa-solid fa-calendar-days"></i></a>
        <a class="sidebar-icon"><i class="fa-solid fa-file-contract"></i></a>
        <a class="sidebar-icon"><i class="fa-solid fa-clock"></i></a>
    </div>
    """, unsafe_allow_html=True)

load_css()

# --- 3. CONTENU PRINCIPAL ---
# On ajoute une marge pour ne pas être caché par la navbar
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# HEADER: "Bonsoir..." et Bouton "Nouvelle demande"
c_head1, c_head2 = st.columns([4, 1])
with c_head1:
    st.markdown("### Bonsoir SAIF-EDDINE 👋")
with c_head2:
    if st.button("+ Nouvelle demande", type="primary"):
        st.toast("Action: Créer une demande")

# GRILLE PRINCIPALE (3 Colonnes)
c1, c2, c3 = st.columns([1, 2.5, 1])

# === COLONNE 1 : PROFIL ===
with c1:
    # Carte Profil
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.markdown("""
        <div class="profile-circle">SB</div>
        <div style="text-align:center; margin-top:15px; font-weight:bold; font-size:16px;">SAIF-EDDINE BOUNOIR</div>
        <div style="text-align:center; color:#888; font-size:13px; margin-bottom:15px;">Responsable commercial<br><span style="font-size:11px">Opérationnel - Racine</span></div>
        <hr style="border:0; border-top:1px solid #eee; margin: 15px 0;">
        <div style="display:flex; justify-content:space-between; font-size:11px; color:#666; margin-bottom:20px;">
            <span><i class="fa-solid fa-location-dot"></i> CASABLANCA</span>
            <span><i class="fa-regular fa-calendar"></i> 22 Aug 2024</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Boutons interactifs
    if st.button("👤 Profil"): st.write("Go Profil")
    if st.button("📅 Calendrier"): st.write("Go Calendrier")
    if st.button("🕒 Tâches"): st.write("Go Tâches")
    if st.button("📄 Documents"): st.write("Go Docs")
    
    st.markdown('</div>', unsafe_allow_html=True) # Fin carte profil

    # Carte Equipe
    st.markdown('<div class="css-card" style="padding:15px;"><b>👥 Mon équipe</b></div>', unsafe_allow_html=True)

# === COLONNE 2 : SUIVI DES DEMANDES ===
with c2:
    st.markdown('<div class="css-card" style="min-height: 500px;">', unsafe_allow_html=True)
    st.markdown('<div style="font-weight:bold; margin-bottom:10px;">Suivi des demandes</div>', unsafe_allow_html=True)
    
    # Onglets Interactifs
    tab1, tab2, tab3, tab4 = st.tabs(["📅 Absences", "📝 Formulaires", "📄 Documents", "💸 Notes de frais"])
    
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        # Empty State
        st.markdown("""
            <div style="text-align:center; padding: 40px; color:#ccc;">
                <div style="font-size:50px; margin-bottom:10px; opacity:0.3;">◯</div>
                <div style="height:10px; width:100px; background:#f0f0f0; margin: 0 auto 10px auto; border-radius:10px;"></div>
                <div style="height:10px; width:140px; background:#f0f0f0; margin: 0 auto; border-radius:10px;"></div>
                <p style="margin-top:20px; font-size:13px; color:#999;">Aucune demande</p>
            </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.info("Aucun formulaire.")
        
    st.markdown('</div>', unsafe_allow_html=True) # Fin carte dashboard
    
    # Carte Bas (Actualités)
    st.markdown("""
    <div class="css-card">
        <div style="display:flex; gap:15px; margin-bottom:15px;">
             <div style="background:#f0f0f0; height:45px; width:45px; border-radius:50%;"></div>
             <div style="background:#f0f0f0; height:20px; width:250px; border-radius:4px; margin-top:12px;"></div>
        </div>
        <div style="display:flex; gap:10px;">
             <div style="background:#f8f9fa; height:80px; flex:1; border-radius:5px;"></div>
             <div style="background:#f8f9fa; height:80px; flex:1; border-radius:5px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# === COLONNE 3 : ANNONCES ===
with c3:
    st.markdown("""
    <div class="css-card" style="height: 500px;">
        <div style="font-weight:bold; margin-bottom:10px;">📢 Annonces</div>
        <hr style="border:0; border-top:1px solid #eee; margin-bottom:20px;">
        <div style="text-align:center; padding-top:100px; color:#aaa;">
            <div style="font-size:50px; margin-bottom:10px; opacity:0.5;">📁</div>
            <div style="font-size:13px;">Aucune annonce à afficher</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) # Fin main-content
