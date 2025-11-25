import json
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# ------------------------ CONFIG STYLES ----------------------------

st.set_page_config(page_title="Messagerie", page_icon="💬", layout="centered")

# CSS CYBERPUNK
page_style = """
<style>
body {
    background-color: #0a0f1f;
}

h1, h2, h3, h4, h5 {
    color: #34d8ff !important;
    text-shadow: 0 0 15px #34d8ff;
    font-weight: 800;
}

.stTextInput>div>div>input {
    background: #111a33;
    color: #d4f2ff !important;
    border: 2px solid #34d8ff;
    border-radius: 8px;
}

.stTextArea textarea {
    background: #111a33;
    border: 2px solid #34d8ff;
    color: #d4f2ff !important;
}

button[kind="primary"] {
    background: linear-gradient(90deg,#00d4ff,#0066ff);
    color: white !important;
    border-radius: 8px;
    border: none !important;
    font-weight: 700;
    box-shadow: 0 0 10px #00d4ff;
}

button[kind="primary"]:hover {
    transform: scale(1.02);
    box-shadow: 0 0 20px #00d4ff;
}

.msg-bubble {
    background: #0f1a33;
    border-left: 4px solid #34d8ff;
    padding: 10px 15px;
    margin: 10px 0;
    border-radius: 5px;
    color: #d4f2ff;
    font-size: 16px;
    box-shadow: 0 0 15px #0f5588;
}

.username {
    color: #00d4ff;
    font-weight: bold;
}
</style>
"""

st.markdown(page_style, unsafe_allow_html=True)

# -------------------------------------------------------------------

st_autorefresh(interval=2000, limit=None, key="auto_refresh")

# Utilisateurs autorisés
user = {"Nawal": "OBXBM3119$", "Akibou": "BLJCUV21810$"}

# Initialiser session_state
if "connecte" not in st.session_state:
    st.session_state["connecte"] = False
if "utilisateur" not in st.session_state:
    st.session_state["utilisateur"] = None

# ------------------------ PAGE CONNEXION ----------------------------

if not st.session_state["connecte"]:
    st.markdown("<h1 style='text-align:center;'>🔐 Portail d'accès sécurisé</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; color:#7befff;'>🛡️ Authentification requise</h3>", unsafe_allow_html=True)

    with st.container():
        nom = st.text_input("👤 Identifiant")
        mot_de_passe = st.text_input("🔑 Mot de passe", type="password")

    if st.button("🚀 Se connecter"):
        if nom in user and user[nom] == mot_de_passe:
            st.session_state["connecte"] = True
            st.session_state["utilisateur"] = nom
            st.rerun()
        else:
            st.error("❌ Identifiant ou mot de passe incorrect.")

# ------------------------ PAGE MESSAGERIE ----------------------------
else:

    st.markdown(f"<h2>👋 Bienvenue, <span style='color:#7de1ff'>{st.session_state['utilisateur']}</span></h2>", unsafe_allow_html=True)

    if st.button("🔓 Déconnexion"):
        st.session_state["connecte"] = False
        st.session_state["utilisateur"] = None
        st.rerun()

    # Charger messages
    try:
        with open("messages.json", "r", encoding="utf-8") as f:
            messages = json.load(f)
    except:
        messages = []

    st.markdown("<h1>💬 Messagerie Privée</h1>", unsafe_allow_html=True)
    st.write("Messages :")

    # Affichage stylé
    for m in messages:
        st.markdown(
            f"""
            <div class='msg-bubble'>
                <span class='username'>{m['nom']}</span> : {m['message']}
            </div>
            """,
            unsafe_allow_html=True
        )

    msg = st.text_area("✏️ Rédige ton message")

    if st.button("📨 Envoyer"):
        if msg.strip() != "":
            messages.append({"nom": st.session_state["utilisateur"], "message": msg})
            with open("messages.json", "w", encoding="utf-8") as f:
                json.dump(messages, f)
            st.success("Message envoyé !")
        else:
            st.warning("Ton message est vide.")
