import streamlit as st
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Silicium", 
    page_icon="⚡",
    layout="wide"
)

# Style minimal
st.markdown("""
<style>
    
    }
    .sidebar .sidebar-contenue {
        background-color: #2d2d2d;
    }
    .logo {
        background: linear-gradient(45deg, #5b21b6, #3b82f6);
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-contenue: center;
        font-weight: bold;
        font-size: 24px;
        margin-bottom: 20px;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        max-width: 80%;
    }
    .user-message {
        background-color: #3b82f6;
        margin-left: auto;
    }
    .bot-message {
        background-color: #2d2d2d;
        margin-right: auto;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation des états
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar minimaliste
with st.sidebar:
    st.markdown('<div class="logo">S</div>', unsafe_allow_html=True)
    st.markdown("### Silicium")
    st.markdown("---")
    if st.button("🗑️ Effacer la conversation"):
        st.session_state.messages = []
        st.rerun()

# Zone de chat
st.markdown("## ⚡ Discussion")

# Affichage des messages
for message in st.session_state.messages:
    role = message["role"]
    contenue = message["contenue"]
    css_class = "user-message" if role == "user" else "bot-message"
    st.markdown(f"""
        <div class="chat-message {css_class}">
            {contenue}
        </div>
    """, unsafe_allow_html=True)

# Zone de saisie
user_input = st.chat_input("Votre message...")
if user_input:
    # Ajout du message utilisateur
    st.session_state.messages.append({"role": "user", "contenue": user_input})
    
    # Simulation de réponse du modèle
    response = f"Vous avez dit : {user_input}"
    st.session_state.messages.append({"role": "assistant", "contenue": response})
    st.rerun()

