import streamlit as st
import speech_recognition as sr
import time

def transcribe_speech(device_index):
    # Create a recognizer object
    r = sr.Recognizer()

    # Flag to indicate if the microphone is active
    is_transcribing = False
    stop_transcription = False

    # Microphone button
    start_button = st.sidebar.button("Start Transcription")
    stop_button = st.sidebar.button("Stop Transcription")
    t = 0

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
    print(sr.Microphone.list_microphone_names())

    # Get the device index from the user
    device_index = st.sidebar.number_input("Enter the input device index", value=0, step=1)

    # Handle the case where the user enters 0 to represent default device index
    if device_index == 0:
        device_index = None

    # Remove "Loading..." message once the app is loaded
    transcribe_speech(device_index)

if __name__ == "__main__":
    main()
