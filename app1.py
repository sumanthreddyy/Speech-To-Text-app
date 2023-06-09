import streamlit as st
import speech_recognition as sr
import time

def transcribe_speech():
    # Create a recognizer object
    r = sr.Recognizer()

    # Flag to indicate if the microphone is active
    is_transcribing = False
    stop_transcription = False

    # Microphone button
    start_button = st.sidebar.button("Start Transcription")
    stop_button = st.sidebar.button("Stop Transcription")
    t = 0

    # Get the list of available input devices
    input_devices = sr.Microphone.list_microphone_names()
    st.write("Available input devices:")
    st.write(input_devices)

    # Specify the correct device index
    device_index = st.sidebar.selectbox("Select input device index:", options=list(range(len(input_devices))))

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

                    # Use the client's microphone as the audio source
                    with sr.Microphone(device_index=device_index) as source:
                        r.adjust_for_ambient_noise(source)
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
                while t < 1:
                    st.info("Click the Transcription button again...")
                    t += 1

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
