import streamlit as st
from streamlit_autorefresh import st_autorefresh
import json


st.set_page_config(page_title="Messagerie", page_icon="💬")

st_autorefresh(interval=2000, limit=None, key="auto_refresh")

# Utilisateurs autorisés
user = {
    "Nawal": "OBXBM3119$",
    "Akibou": "BLJCUV21810$"
}

# Initialiser session_state
if "connecte" not in st.session_state:
    st.session_state["connecte"] = False
if "utilisateur" not in st.session_state:
    st.session_state["utilisateur"] = None

# --- Page connexion ---
if not st.session_state["connecte"]:
    st.title("🔐 Connexion à la messagerie")
    nom = st.text_input("User name")
    mot_de_passe = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if nom in user and user[nom] == mot_de_passe:
            st.session_state["connecte"] = True
            st.session_state["utilisateur"] = nom
            st.rerun() # recharge la page après connexion
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")

# --- Page messagerie ---
else:

    st.success(f"Bienvenue {st.session_state['utilisateur']} !")

    if st.button("Déconnexion"):
        st.session_state["connecte"] = False
        st.session_state["utilisateur"] = None
        st.rerun()

    # Charger messages
    try:
        with open("messages.json", "r", encoding="utf-8") as f:
            messages = json.load(f)
    except:
        messages = []

    st.title("💬 Messagerie perso avec Papa")

    msg = st.text_area("Écris ton message ici :")

    if st.button("Envoyer"):
        messages.append({
            "nom": st.session_state["utilisateur"],
            "message": msg
        })
        with open("messages.json", "w", encoding="utf-8") as f:
            json.dump(messages, f)
        st.success("Message envoyé !")

    st.write("💬 Messages :")
    for m in messages:
        st.write(f"**{m['nom']}** : {m['message']}")
