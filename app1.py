import streamlit as st
import speech_recognition as sr
import time
import pyaudio

def transcribe_speech(device_index):
    # Create a recognizer object
    r = sr.Recognizer()

    # Use the default microphone as the audio source
    try:
        mic = sr.Microphone(device_index=device_index)
    except OSError as e:
        st.error(f"Error: {e}")
        st.error("No input devices available.")
        return

    # Adjust the microphone for ambient noise
    with mic as source:
        r.adjust_for_ambient_noise(source)

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
                while t < 1:
                    st.info("Click the Transcription button again...")
                    t = t + 1

            if stop_transcription:
                # Transcription stopped, break the loop
                break

            time.sleep(0.1)

        except sr.UnknownValueError:
            # Ignore any unrecognized speech
            pass


def main():
    st.title("Real-time Voice Transcription")

    # Get the available audio devices
    def get_available_devices():
        audio = pyaudio.PyAudio()
        device_count = audio.get_device_count()
        devices = []

        for i in range(device_count):
            device_info = audio.get_device_info_by_index(i)
            devices.append(device_info["name"])

        return devices

    devices = get_available_devices()

    # Display the available audio devices in the sidebar
    if len(devices) > 0:
        selected_device_index = st.sidebar.selectbox("Select Microphone", range(len(devices)))
    else:
        st.sidebar.error("No input devices available.")
        return

    # Remove "Loading..." message once the app is loaded
    transcribe_speech(selected_device_index)


if __name__ == "__main__":
    main()
