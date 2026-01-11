import streamlit as st
import pandas as pd
import utils
from datetime import date, timedelta

st.set_page_config(page_title="Planning", page_icon="🗓️", layout="wide")
utils.apply_style()
utils.check_auth()

st.title("🗓️ Planning & Timesheet")
user = st.session_state.user

# Admin peut voir tout le monde, User voit que lui
target_user = user['username']
if user['role'] == 'admin':
    users = utils.load_data(utils.USERS_FILE)
    target_user = st.selectbox("Voir planning de :", users['username'].tolist())

# Selecteur Date
d = st.date_input("Semaine du", date.today() - timedelta(days=date.today().weekday()))
monday = d - timedelta(days=d.weekday())

# Chargement données
df_plan = utils.load_data(utils.PLANNING_FILE)
week_days = [monday + timedelta(days=i) for i in range(7)]

# Construction Données Editeur
editor_data = []
for day in week_days:
    d_str = day.strftime("%Y-%m-%d")
    existing = df_plan[(df_plan['username'] == target_user) & (df_plan['date'] == d_str)]
    
    if not existing.empty:
        row = existing.iloc[0]
        editor_data.append({"Date": d_str, "Statut": row['status'], "Début": row['start_time'], "Fin": row['end_time'], "Pause": int(row['break_min'])})
    else:
        is_weekend = day.weekday() >= 5
        editor_data.append({"Date": d_str, "Statut": "Repos" if is_weekend else "Travail", "Début": "-" if is_weekend else "09:00", "Fin": "-" if is_weekend else "18:00", "Pause": 0 if is_weekend else 60})

# Affichage Tableau
edited = st.data_editor(pd.DataFrame(editor_data), key="plan_edit", use_container_width=True, hide_index=True)

if st.button("💾 Sauvegarder"):
    # Logique de sauvegarde (simplifiée)
    week_str = [x['Date'] for x in editor_data]
    df_plan = df_plan[~((df_plan['username'] == target_user) & (df_plan['date'].isin(week_str)))]
    
    new_rows = []
    for idx, row in edited.iterrows():
        new_rows.append({"username": target_user, "date": row['Date'], "status": row['Statut'], "start_time": row['Début'], "end_time": row['Fin'], "break_min": row['Pause']})
    
    utils.save_data(pd.concat([df_plan, pd.DataFrame(new_rows)], ignore_index=True), utils.PLANNING_FILE)
    st.success("Planning sauvegardé !")
