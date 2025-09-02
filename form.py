import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import io
import os


# parametre page
st.set_page_config(page_title="Formuulaire pour CV")

# grand titre au debur de la page
st.header("Formulaire de votre CV")

# Initialisation de la session de la page
with st.form("CV form"):

    # Renseignement des champs du formulaire
    nom = st.text_input("Nom")
    prenom = st.text_input("Prenom")
    email = st.text_input("Email")
    telephone = st.text_input("Telephone")
    experience = st.text_area("Experience professionnelles")
    formation = st.text_area("Formation")
    competences = st.text_area("Competences")
    langues = st.text_area("Langues")
    st.form_submit_button("Envoyer", on_click=lambda: st.session_state.update())


# , profil, photo_path=None
# --- Fonction pour créer un CV stylé ---
def creer_cv_pdf(nom, email, telephone, experience, competences):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    # Marges
    largeur, hauteur = A4
    x_margin = 2 * cm
    y_margin = hauteur - 2 * cm

    # # Photo de profil (si fournie)
    # if photo_path and os.path.exists(photo_path):
    #     c.drawImage(photo_path, largeur - 5*cm, hauteur - 4*cm, width=3.5*cm, height=3.5*cm, mask='auto')

    # Nom
    c.setFont("Helvetica-Bold", 22)
    c.drawString(x_margin, y_margin, nom)

    # Coordonnées
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.grey)
    c.drawString(x_margin, y_margin - 20, f"Email : {email}  |  Téléphone : {telephone}")
    c.setFillColor(colors.black)

    # # Profil
    # c.setFont("Helvetica-Bold", 14)
    # c.setFillColor(colors.HexColor("#007BFF"))
    # c.drawString(x_margin, y_margin - 50, "Profil")
    # c.setFillColor(colors.black)
    # c.setFont("Helvetica", 12)
    # text_obj = c.beginText(x_margin, y_margin - 70)
    # for ligne in profil.split("\n"):
    #     text_obj.textLine(ligne)
    # c.drawText(text_obj)

    # Expérience
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.HexColor("#007BFF"))
    c.drawString(x_margin, y_margin - 120, "Expérience professionnelle")
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 12)
    text_obj = c.beginText(x_margin, y_margin - 140)
    for ligne in experience.split("\n"):
        text_obj.textLine(ligne)
    c.drawText(text_obj)

    # Compétences
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.HexColor("#007BFF"))
    c.drawString(x_margin, y_margin - 250, "Compétences")
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 12)
    text_obj = c.beginText(x_margin, y_margin - 270)
    for ligne in competences.split("\n"):
        text_obj.textLine("• " + ligne)
    c.drawText(text_obj)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer


# Sauvegarde temporaire de la photo
# """ photo_path = None
# if photo:
#     photo_path = f"temp_{photo.name}"
#     with open(photo_path, "wb") as f:
#         f.write(photo.read())
#  """
# , profil, photo_path
if st.button("📄 Générer le CV PDF"):
    pdf_buffer = creer_cv_pdf(nom, email, telephone, experience, competences)
    st.download_button(
        label="📥 Télécharger le CV",
        data=pdf_buffer,
        file_name=f"{nom.replace(' ', '_')}_CV.pdf",
        mime="application/pdf"
    )

# Suppression du fichier temporaire
""" if photo_path and os.path.exists(photo_path):
    os.remove(photo_path) """

