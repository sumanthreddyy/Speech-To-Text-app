import streamlit as st
import speech_recognition as sr
import time

def transcribe_speech(device_index):
    
    # Create a recognizer object
    r = sr.Recognizer()
    mic = sr.Microphone(device_index=device_index)
    # Use the default microphone as the audio source
    mic = sr.Microphone()

    # Adjust the microphone for ambient noise
    with mic as source:
        r.adjust_for_ambient_noise(source)

    # Flag to indicate if the microphone is active
    is_transcribing = False
    stop_transcription = False

    # Microphone button
    start_button = st.sidebar.button("Start Transcription")
    stop_button = st.sidebar.button("Stop Transcription")
    t=0
    # Continuously transcribe audio input
    while True:
        try:
            if start_button:
                if not is_transcribing:
                    # Start transcription
                    is_transcribing = True
                    stop_transcription = False
                    start_button = False  # Disable the Start button
                    st.info("Listening...")

                    with mic as source:
                        audio_data = r.listen(source)

                    # Recognize speech using Google Speech Recognition
                    text = r.recognize_google(audio_data)

                    # Display the transcribed text in the Streamlit app
                    if text.strip():  # Check if the text is not empty
                        st.write(text)

                else:
                    
                    # Transcription already started
                    pass
                   
            elif stop_button:
                # Stop transcription
                stop_transcription = True
                is_transcribing = False
                stop_button = False  # Disable the Stop button
                st.warning("Transcription Stopped")
                break  # Exit the loop to stop transcription

            else:
                while t<1:
                    st.info("Click the Transcription button again...")
                    t=t+1

            if stop_transcription:
                # Transcription stopped, break the loop
                break

            time.sleep(0.1)

        except sr.UnknownValueError:
            # Ignore any unrecognized speech
            pass

def main():
    st.title("Real-time Voice Transcription")
    device_index = st.sidebar.number_input("Microphone Device Index", min_value=0, max_value=10, value=0, step=1)
    transcribe_speech(device_index)
    # Remove "Loading..." message once the app is loaded


if __name__ == "__main__":
    main()
