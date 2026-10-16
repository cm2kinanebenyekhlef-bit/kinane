import streamlit as st
import yt_dlp
import os
from pathlib import Path

# --- CONFIGURATION DU CODE SECRET ---
# Modifiez ce mot de passe par celui de votre choix
CODE_SECRET = "Soulfly2026"

st.set_page_config(page_title="YouTube Downloader Privé", page_icon="🔒", layout="centered")

# Initialisation de l'état de connexion si non présent
if "authentifie" not in st.session_state:
    st.session_state["authentifie"] = False

# --- INTERFACE DE VÉRIFICATION DU CODE ---
if not st.session_state["authentifie"]:
    st.title("🔒 Accès Restreint")
    st.write("Veuillez saisir le code d'accès pour utiliser le convertisseur.")

    code_saisi = st.text_input("Code d'accès :", type="password")
    valider = st.button("Valider")

    if valider:
        if code_saisi == CODE_SECRET:
            st.session_state["authentifie"] = True
            st.rerun()
        else:
            st.error("Code incorrect. Accès refusé.")

# --- INTERFACE PRINCIPALE (S'AFFICHE UNIQUEMENT SI LE CODE EST BON) ---
else:
    st.title("🎬 YouTube Video Downloader (Privé)")

    # Bouton de déconnexion
    if st.sidebar.button("Se déconnecter"):
        st.session_state["authentifie"] = False
        st.rerun()

    # NOTE POUR LE CLOUD : Sur un serveur en ligne, le dossier "Bureau" n'existe pas.
    # On télécharge donc dans le dossier temporaire du serveur pour permettre le téléchargement local ensuite.
    st.write("Entrez l'URL d'une vidéo YouTube ci-dessous.")

    url = st.text_input("URL de la vidéo :", placeholder="https://youtube.com...")

    if st.button("Télécharger la vidéo"):
        if not url.strip():
            st.error("Veuillez entrer une URL valide.")
        else:
            statut = st.empty()
            statut.info("Téléchargement en cours sur le serveur...")

            ydl_opts = {
                'format': 'best',
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'web_safari']
                    }
                },
                'outtmpl': '%(title)s.%(ext)s'
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    nom_fichier = ydl.prepare_filename(info)

                statut.success("🔥 Vidéo récupérée avec succès par le serveur !")

                # Interface pour envoyer le fichier du serveur vers l'ordinateur de l'utilisateur
                if os.path.exists(nom_fichier):
                    with open(nom_fichier, "rb") as file:
                        st.download_button(
                            label="💾 Enregistrer la vidéo sur votre appareil",
                            data=file,
                            file_name=os.path.basename(nom_fichier),
                            mime="video/mp4"
                        )
                    # Nettoyage du fichier sur le serveur après mise à disposition
                    os.remove(nom_fichier)

            except Exception as e:
                statut.error(f"Une erreur est survenue : {e}")