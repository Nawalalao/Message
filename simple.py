import streamlit as st


verbe = ["manger", "boire", "dormir", "courir", "lire", "ecrire", "parler", "ecouter", "regarder"]

if "index" not in st.session_state:
    st.session_state["index"] = 0

if st.button("Changer de verbe"):
    st.session_state["index"] = (st.session_state["index"] + 1) % len(verbe)

st.write(f"Tu as choisi le verbe: {verbe[st.session_state['index']]}")
