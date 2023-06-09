import streamlit as st
import streamlit_webrtc as webrtc
import speech_recognition as sr

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

    # Create a WebRTC microphone input
    webrtc_ctx = webrtc.VideoTransformerBase(
        transform_func=None,
        fps=30,
    )

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

                # Get the audio frames from the WebRTC microphone input
                for audio_frames in webrtc_ctx.generator():
                    audio_data = b"".join([frame.to_ndarray() for frame in audio_frames])
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
                st.info("Click the Start Transcription button...")
            else:
                st.info("Transcription in progress...")

        if stop_button:
            # Stop transcription
            is_transcribing = False
            stop_button = False  # Disable the Stop button
            st.warning("Transcription Stopped")
            break  # Exit the loop to stop transcription

def request_microphone_access():
    webrtc_ctx = webrtc.VideoTransformerBase(
        transform_func=None,
        fps=30,
    )
    webrtc_ctx.request_media_stream_constraints(audio=True)

def initialize_app():
    st.title("Real-time Voice Transcription")
    st.sidebar.button("Grant Microphone Access", on_click=request_microphone_access)

def check_microphone_access():
    webrtc_ctx = webrtc.VideoTransformerBase(
        transform_func=None,
        fps=30,
    )
    return webrtc_ctx.state.playing

if __name__ == "__main__":
    if check_microphone_access():
        main()
    else:
        initialize_app()
