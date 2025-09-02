import streamlit as st

recap = {
    "Nom": "",
    "Date de debut": "",
    "Date de fin": "",
    "Horaire": "",
    "Objectives": [],
    "Status": "En cours",
    "Importance": 0,
    "Urgence": 0,
}

with st.form("Start!"):
    nom = st.text_input(label="Nom")
    recap["Nom"] = nom
    date_debut = st.date_input(label="Date de debut")
    recap['Date de debut'] = date_debut
    date_fin = st.date_input(label="Date de fin")
    recap["Date de fin"]=date_fin
    horaire = st.time_input(label="Horaire")
    recap["Horaire"] = horaire
    importance = st.slider(label="Importance", min_value=0, max_value=10, value=5)
    recap["Importance"] = importance
    urgence = st.slider(label="urgence", min_value=0, max_value=10, value=5)
    recap["Urgence"] = urgence
    objectifs = st.text_area(label="Objectives", placeholder="Entrer vos objectives ici...")
    recap["Objectives"] = objectifs.splitlines()
    st.form_submit_button("Valider", on_click=lambda:st.session_state.update(recap))
    st.write("Formulaire soumis avec succes!")
