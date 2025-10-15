import streamlit as st
import speech_recognition as sr
import sounddevice as sd
import soundfile as sf
import numpy as np
import tempfile
import nltk
from nltk.chat.util import Chat, reflections

# Télécharger les ressources NLTK
nltk.download('punkt')

# Définir les dialogues
pairs = [
    ["bonjour", ["Bonjour ! Comment puis-je vous aider aujourd'hui ?"]],
    ["comment ça va ?", ["Je vais bien, merci ! Et vous ?"]],
    ["quel est ton nom ?", ["Je suis un chatbot vocal créé pour vous aider."]],
    ["au revoir", ["Au revoir ! Passez une bonne journée."]],
    ["(.*)", ["Désolé, je n'ai pas compris cela. Pouvez-vous reformuler ?"]]
]

chatbot = Chat(pairs, reflections)

# Fonction pour la reconnaissance vocale SANS PyAudio
def recognize_speech():
    samplerate = 16000
    duration = 5  # secondes
    st.info("Parlez maintenant...")

    # Enregistrer l'audio avec sounddevice
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()

    # Sauvegarde dans un fichier temporaire WAV
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        sf.write(tmpfile.name, recording, samplerate)
        tmpfile_path = tmpfile.name

    # Utiliser SpeechRecognition sur le fichier audio
    recognizer = sr.Recognizer()
    with sr.AudioFile(tmpfile_path) as source:
        audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio, language="fr-FR")
        except sr.UnknownValueError:
            return "Désolé, je n'ai pas compris."
        except sr.RequestError:
            return "Erreur de service de reconnaissance vocale."

# Interface Streamlit
st.title("🤖 Chatbot Vocal")

mode = st.radio("Choisissez le mode d'entrée :", ("Texte", "Vocal"))

if mode == "Texte":
    user_input = st.text_input("Tapez votre message :")
    if user_input:
        response = chatbot.respond(user_input)
        st.text_area("Réponse du Chatbot :", value=response, height=100)
else:
    if st.button("🎤 Parler maintenant"):
        user_input = recognize_speech()
        st.text("Vous avez dit : " + user_input)
        response = chatbot.respond(user_input)
        st.text_area("Réponse du Chatbot :", value=response, height=100)
