import streamlit as st
import speech_recognition as sr

def transcribe_speech(device_index):
    # Create a recognizer object
    r = sr.Recognizer()

    # Use the selected microphone as the audio source
    mic = sr.Microphone(device_index=device_index)

    # Adjust the microphone for ambient noise
    with mic as source:
        r.adjust_for_ambient_noise(source)

    # Start transcription
    st.info("Listening...")

    with mic as source:
        audio_data = r.listen(source)

    # Recognize speech using Google Speech Recognition
    text = r.recognize_google(audio_data)

    # Display the transcribed text in the Streamlit app
    if text.strip():  # Check if the text is not empty
        st.write(text)


def main():
    st.title("Real-time Voice Transcription")

    # Get the list of available microphones
    microphone_list = sr.Microphone.list_microphone_names()

    # Create a dropdown list for microphone selection
    device_index = st.sidebar.selectbox("Select Microphone", microphone_list)

    # Start transcription button
    if st.sidebar.button("Start Transcription"):
        transcribe_speech(device_index)


if __name__ == "__main__":
    main()
