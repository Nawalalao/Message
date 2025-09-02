import streamlit as st

st.set_page_config(page_title="S-Appli",
                   )

objective = []

st.header("Welcome :), ")

st.subheader("Commencons let's go!")

st.code("FocusObjective")

st.markdown("---")

st.session_state.objectifs = []

def ok():
    objet = str(st.session_state.objectif)
    st.session_state.objectifs.append(objet)
    st.session_state.objectif = ""

Entrer = st.text_input(
    label="Entrez vos objectifs: ",
    key="objectif",
    on_change=ok
)

n = st.button(label="Terminer!")

if n:
    if st.session_state.objectifs:
        st.write("📜 Liste finale :")
        for i, texte in enumerate(st.session_state.objectifs, start=1):
            st.write(f"{i}. {texte}")
    else:
        st.warning("Aucun texte saisi pour le moment.")

st.markdown("### A faire")


tab1, tab2, tab3 = st.tabs(["Level1", "level2", "level3"])
    
with tab1:
    st.subheader("Date de debut")
    date_debut = st.date_input(label="Debut...")

with tab2:
    st.subheader("Date de fin")
    st.fin = st.date_input(label="Fin...", )

with tab3:
    st.subheader("Horaire")
    st.time_input(label="Temps...", )

