import streamlit as st
import utils

st.set_page_config(page_title="Mon Profil", page_icon="👤", layout="wide")
utils.apply_style()
utils.check_auth() # Sécurité

st.title("👤 Mon Profil")
user = st.session_state.user

with st.form("profile_form"):
    c1, c2 = st.columns(2)
    addr = c1.text_input("Adresse", user.get('address',''))
    phone = c2.text_input("Téléphone", user.get('phone',''))
    pwd = c1.text_input("Nouveau mot de passe", type="password")
    
    if st.form_submit_button("Mettre à jour"):
        df = utils.load_data(utils.USERS_FILE)
        idx = df[df['username'] == user['username']].index[0]
        df.at[idx, 'address'] = addr
        df.at[idx, 'phone'] = phone
        if pwd: df.at[idx, 'password'] = pwd
        utils.save_data(df, utils.USERS_FILE)
        
        # Update session state
        st.session_state.user = df.iloc[idx]
        st.success("Profil mis à jour !")
