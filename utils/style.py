/* assets/style.css */

/* --- VARIABLES YASSIR --- */
:root {
    --primary-purple: #6200EE; /* Violet Yassir */
    --bg-color: #F4F6F9;
    --card-bg: #ffffff;
    --text-dark: #333333;
    --text-grey: #6c757d;
    --border-color: #e0e0e0;
}

/* --- RESET & CONFIGURATION GLOBALE STREAMLIT --- */
.stApp {
    background-color: var(--bg-color);
    font-family: 'Poppins', 'Segoe UI', sans-serif;
}

/* Cacher les éléments natifs de Streamlit */
#MainMenu, header, footer { visibility: hidden; }
.block-container {
    padding-top: 0 !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
    max-width: 100% !important;
}

/* --- NAVBAR DU HAUT (VIOLET) --- */
.top-navbar {
    background-color: var(--primary-purple);
    height: 60px;
    width: 100%;
    position: fixed;
    top: 0; left: 0; z-index: 9999;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 20px; color: white;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.search-container input {
    background: rgba(255,255,255,0.2);
    border: none;
    padding: 8px 15px;
    border-radius: 4px;
    color: white;
    width: 350px;
    outline: none;
}
.search-container input::placeholder { color: rgba(255,255,255,0.7); }

/* --- SIDEBAR GAUCHE (ICONES) --- */
.left-sidebar {
    background-color: white;
    width: 70px;
    height: 100vh;
    position: fixed; top: 60px; left: 0; z-index: 9998;
    display: flex; flex-direction: column; align-items: center;
    padding-top: 20px;
    border-right: 1px solid var(--border-color);
    box-shadow: 2px 0 5px rgba(0,0,0,0.02);
}

.sidebar-icon {
    font-size: 20px;
    color: #9aa0ac;
    margin-bottom: 30px;
    cursor: pointer;
    transition: 0.2s;
    text-decoration: none;
}
.sidebar-icon:hover { color: var(--primary-purple); transform: scale(1.1); }
.sidebar-icon.active { color: var(--primary-purple); border-right: 3px solid var(--primary-purple); }

/* --- CONTENU PRINCIPAL (PADDING POUR ÉVITER LE CHEVAUCHEMENT) --- */
.main-content {
    margin-top: 60px;
    margin-left: 70px;
    padding: 30px;
}

/* --- CARTES (CARDS) --- */
.css-card {
    background-color: white;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    border: 1px solid #eaeaea;
    margin-bottom: 20px;
    height: 100%;
}

/* --- PROFIL CERCLE --- */
.profile-circle {
    width: 90px; height: 90px; margin: 0 auto;
    border-radius: 50%;
    background: var(--primary-purple);
    color: white;
    display: flex; align-items: center; justify-content: center;
    font-size: 28px; font-weight: 500;
    border: 4px solid white;
    box-shadow: 0 0 0 2px var(--primary-purple);
}

/* --- BOUTONS NAVIGATION PROFIL (Gris) --- */
div.stButton > button {
    width: 100%;
    text-align: left;
    background-color: #f8f9fa;
    border: none;
    color: #555;
    padding: 10px 15px;
    margin-bottom: 0px;
    border-radius: 6px;
    font-size: 13px;
    transition: 0.2s;
}
div.stButton > button:hover {
    background-color: #eef2ff;
    color: var(--primary-purple);
}
div.stButton > button:focus {
    box-shadow: none;
    border: 1px solid var(--primary-purple);
}

/* --- BOUTON PRINCIPAL "NOUVELLE DEMANDE" --- */
/* On cible spécifiquement le bouton dans la colonne de droite */
div[data-testid="column"]:nth-child(2) div.stButton > button {
    background-color: var(--primary-purple);
    color: white;
    text-align: center;
    font-weight: bold;
}
div[data-testid="column"]:nth-child(2) div.stButton > button:hover {
    background-color: #4a00b0;
    color: white;
}

/* --- TABS (ONGLETS) STYLE YASSIR --- */
.stTabs [data-baseweb="tab-list"] {
    gap: 20px;
    border-bottom: 1px solid #eee;
    padding-bottom: 0;
}
.stTabs [data-baseweb="tab"] {
    height: 50px;
    white-space: pre-wrap;
    background-color: transparent;
    border: none;
    color: #666;
    font-weight: 500;
    font-size: 14px;
}
.stTabs [aria-selected="true"] {
    color: var(--primary-purple) !important;
    border-bottom: 2px solid var(--primary-purple) !important;
    font-weight: bold;
}

/* --- BADGES (Petites pastilles vertes) --- */
.badge-count {
    background-color: #00C853;
    color: white;
    padding: 2px 6px;
    border-radius: 10px;
    font-size: 10px;
    margin-left: 5px;
    vertical-align: middle;
}
