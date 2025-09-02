import streamlit as st
import time

st.set_page_config(page_title="Your goals", page_icon="🎯", layout="wide")
st.title('Focus Objective tracker')
st.write("Welcome to the Focus Objectives tracker app! This app helps you set and track your objectives effectively.")

pages = {
    "Accueil": [st.Page("home.py", title="Tableau de bord", icon="🏠")],
    "Objectifs": [st.Page("goals.py", title="Mes objectifs", icon="🎯")]
}
pg = st.navigation(pages, position="sidebar")
pg.run()
