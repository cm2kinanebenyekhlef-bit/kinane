import streamlit as st
import yt_dlp
import os

CODE_SECRET = "Soulfly2026"

st.set_page_config(page_title="YouTube MP3 Downloader Privé", page_icon="🔒", layout="centered")

if "authentifie" not in st.session_state:
    st.session_state["authentifie"] = False

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

else:
    st.title("🎵 YouTube MP3 Downloader (Spécial Cloud)")
    st.write("Ce mode extrait uniquement l'audio pour contourner les blocages pare-feu de YouTube.")
    
    if st.sidebar.button("Se déconnecter"):
        st.session_state["authentifie"] = False
        st.rerun()

    url = st.text_input("URL de la vidéo :", placeholder="https://www.youtube.com/watch?v=...")

    if st.button("Extraire l'audio (MP3)"):
        if not url.strip():
            st.error("Veuillez entrer une URL valide.")
        else:
            statut = st.empty()
            statut.info("Extraction du flux audio en cours sur le serveur...")

            # Configuration stricte Audio + Impersonation pour masquer le serveur Streamlit
            ydl_opts = {
                'format': 'bestaudio/best',
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
                },
                'outtmpl': '%(title)s.%(ext)s',
                'no_warnings': True,
                'quiet': True
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    nom_fichier = ydl.prepare_filename(info)
                
                statut.success("🔥 Flux audio récupéré avec succès !")
                
                if os.path.exists(nom_fichier):
                    with open(nom_fichier, "rb") as file:
                        st.download_button(
                            label="💾 Enregistrer le fichier audio",
                            data=file,
                            file_name=f"{info.get('title')}.mp3",
                            mime="audio/mp3"
                        )
                    os.remove(nom_fichier)
                    
            except Exception as e:
                statut.error(f"Une erreur est survenue : {e}")
