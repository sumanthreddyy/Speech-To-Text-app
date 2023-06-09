import streamlit as st
import speech_recognition as sr
t=0
def transcribe_speech(audio_data):
    # Create a recognizer object
    r = sr.Recognizer()

    # Recognize speech using Google Speech Recognition
    text = r.recognize_google(audio_data)

    # Display the transcribed text in the Streamlit app
    if text.strip():  # Check if the text is not empty
        st.write(text)

def main():
    st.title("Real-time Voice Transcription")

    # Flag to indicate if the microphone is active
    is_transcribing = False

    # Microphone button
    start_button = st.sidebar.button("Start Transcription")
    stop_button = st.sidebar.button("Stop Transcription")

    # Continuously transcribe audio input
    while True:
        if start_button:
            if not is_transcribing:
                # Start transcription
                is_transcribing = True
                start_button = False  # Disable the Start button
                st.info("Listening...")

                # Start microphone input
                with sr.Microphone() as source:
                    audio_data = sr.Recognizer().listen(source)
                transcribe_speech(audio_data)

                # Check if Stop button is clicked
                if stop_button:
                    is_transcribing = False
                    stop_button = False  # Disable the Stop button
                    st.warning("Transcription Stopped")
                    break  # Exit the loop to stop transcription
            else:
                # Transcription already started
                pass
        else:
            if not is_transcribing:
                while t<1:
                st.info("Click the Start Transcription button...")
                t+=1
            else:
                st.info("Transcription in progress...")

        if stop_button:
            # Stop transcription
            is_transcribing = False
            stop_button = False  # Disable the Stop button
            st.warning("Transcription Stopped")
            break  # Exit the loop to stop transcription

if __name__ == "__main__":
    main()
