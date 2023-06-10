import streamlit as st
import speech_recognition as sr
import time

def check_microphone_access():
    # Create a recognizer object
    r = sr.Recognizer()

    # Get available microphones
    mic_list = sr.Microphone.list_microphone_names()

    # Display microphone selection dropdown
    selected_mic = st.sidebar.selectbox("Select Microphone", mic_list)

    if selected_mic:
        # Use the selected microphone as the audio source
        mic = sr.Microphone(device_index=mic_list.index(selected_mic))

        # Check if the microphone access is available
        with mic as source:
            try:
                r.adjust_for_ambient_noise(source)
                return True
            except sr.RequestError:
                return False
    else:
        return False

def transcribe_speech():
    # Create a recognizer object
    r = sr.Recognizer()

    # Flag to indicate if the microphone is active
    is_transcribing = False
    stop_transcription = False

    # Microphone button
    start_button = st.sidebar.button("Start Transcription")
    stop_button = st.sidebar.button("Stop Transcription")

    # Check microphone access
    microphone_access = check_microphone_access()

    if not microphone_access:
        st.error("Microphone access not available. Please check your microphone settings.")
        return

    # Adjust the microphone for ambient noise
    mic = sr.Microphone()

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

            if stop_transcription:
                # Transcription stopped, break the loop
                break

            time.sleep(0.1)

        except sr.UnknownValueError:
            # Ignore any unrecognized speech
            pass

def main():
    st.title("Real-time Voice Transcription")
    
    # Remove "Loading..." message once the app is loaded
    transcribe_speech()

if __name__ == "__main__":
    main()
