import streamlit as st

CODE_SECRET = "Soulfly2026"

st.set_page_config(page_title="YouTube Bypass Downloader", page_icon="🔒", layout="centered")

if "authentifie" not in st.session_state:
    st.session_state["authentifie"] = False

if not st.session_state["authentifie"]:
    st.title("🔒 Accès Restreint")
    st.write("Veuillez saisir le code d'accès pour débloquer le téléchargeur.")
    
    code_saisi = st.text_input("Code d'accès :", type="password")
    valider = st.button("Valider")
    
    if valider:
        if code_saisi == CODE_SECRET:
            st.session_state["authentifie"] = True
            st.rerun()
        else:
            st.error("Code incorrect. Accès refusé.")

else:
    st.title("🎬 Décodeur YouTube Universel (Anti-403)")
    st.write("Les serveurs Cloud étant bloqués par YouTube, voici la méthode universelle pour télécharger instantanément sans erreur.")
    
    if st.sidebar.button("Se déconnecter"):
        st.session_state["authentifie"] = False
        st.rerun()

    st.markdown("### 🛠️ Mode d'emploi en 2 étapes :")
    
    # Code JavaScript du Bookmarklet
    bookmarklet_code = (
        "javascript:(function(){"
        "var url = window.location.href;"
        "if(url.indexOf('://youtube.com') !== -1 || url.indexOf('youtu.be/') !== -1){"
        "window.open('https://9xbuddy.in' + encodeURIComponent(url), '_blank');"
        "}else{"
        "alert('Ouvrez d\'abord une vidéo YouTube avant de cliquer ici !');"
        "}"
        "})();"
    )
    
    st.write("1. **Glissez-déposez** le bouton vert ci-dessous directement dans la **barre des favoris / marque-pages** de votre navigateur internet :")
    
    # Correction ici : Utilisation du paramètre correct unsafe_allow_html=True
    st.markdown(
        f'<a href="{bookmarklet_code}" style="display: inline-block; padding: 15px 25px; '
        f'font-size: 16px; font-weight: bold; color: white; background-color: #28a745; '
        f'text-align: center; text-decoration: none; border-radius: 8px; cursor: move;">'
        f'🚀 TELECHARGER LA VIDEO</a>', 
        unsafe_allow_html=True
    )
    
    st.write("")
    st.write("2. **Allez sur YouTube**, ouvrez la vidéo de votre choix, puis **cliquez simplement sur ce favori** dans votre barre de navigation.")
    st.info("Un nouvel onglet sécurisé va s'ouvrir, décodant la vidéo instantanément grâce à votre propre connexion internet, éliminant définitivement l'erreur 403.")
