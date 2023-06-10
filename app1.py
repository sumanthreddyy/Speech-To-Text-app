import streamlit as st
import speech_recognition as sr
import time
import av
import numpy as np
from webrtc_streamer import webrtc_streamer, VideoTransformerBase

class AudioTransformer(VideoTransformerBase):
    def transform(self, frame):
        audio = frame.to_ndarray(format="s16")
        return audio

def transcribe_speech():
    # Create a recognizer object
    r = sr.Recognizer()

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

                    # WebRTC audio stream
                    webrtc_ctx = webrtc_streamer(
                        key="example",
                        mode=webrtc_streamer.WebRtcMode.SENDRECV,
                        audio_transformer_factory=AudioTransformer,
                        async_transform=True,
                    )

                    # Continuously process audio frames
                    for audio_frame in webrtc_ctx.audio_frames():
                        audio_data = np.frombuffer(audio_frame.to_ndarray(), dtype=np.int16)

                        # Recognize speech using Google Speech Recognition
                        text = r.recognize_google(audio_data)

                        # Display the transcribed text in the Streamlit app
                        if text.strip():  # Check if the text is not empty
                            st.write(text)

                        if stop_transcription:
                            # Transcription stopped, break the loop
                            break

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
