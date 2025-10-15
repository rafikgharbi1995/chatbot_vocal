import streamlit as st
import nltk
from nltk.chat.util import Chat, reflections
import os

nltk.download('punkt')

pairs = [
    ["bonjour", ["Bonjour ! Comment puis-je vous aider aujourd'hui ?"]],
    ["comment ça va ?", ["Je vais bien, merci ! Et vous ?"]],
    ["quel est ton nom ?", ["Je suis un chatbot vocal créé pour vous aider."]],
    ["au revoir", ["Au revoir ! Passez une bonne journée."]],
    ["(.*)", ["Désolé, je n'ai pas compris cela. Pouvez-vous reformuler ?"]]
]

chatbot = Chat(pairs, reflections)

# Détection si on est sur Streamlit Cloud
ON_STREAMLIT_CLOUD = os.environ.get("STREAMLIT_RUNTIME", "") != ""

st.title("🤖 Chatbot Vocal")

if ON_STREAMLIT_CLOUD:
    st.warning("Le mode vocal n'est pas disponible sur Streamlit Cloud.")
    mode = "Texte"
else:
    import speech_recognition as sr

    def recognize_speech():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Parlez maintenant...")
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio, language="fr-FR")
                return text
            except sr.UnknownValueError:
                return "Désolé, je n'ai pas compris."
            except sr.RequestError:
                return "Erreur de service de reconnaissance vocale."

    mode = st.radio("Choisissez le mode d'entrée :", ("Texte", "Vocal"))

if mode == "Texte":
    user_input = st.text_input("Tapez votre message :")
    if user_input:
        response = chatbot.respond(user_input)
        st.text_area("Réponse du Chatbot :", value=response, height=100)

elif mode == "Vocal":
    if st.button("🎤 Parler maintenant"):
        user_input = recognize_speech()
        st.text("Vous avez dit : " + user_input)
        response = chatbot.respond(user_input)
        st.text_area("Réponse du Chatbot :", value=response, height=100)
