from flask import Flask, render_template
from flask_webrtc import (
    WebRTCAudioStream,
    RTCSessionDescription,
    RTCIceCandidate,
)
import av
import numpy as np
import speech_recognition as sr

app = Flask(__name__)
r = sr.Recognizer()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/offer", methods=["POST"])
def offer():
    offer = RTCSessionDescription.sdp(request.json)
    pc = WebRTCAudioStream()
    @pc.on("track")
    def on_track(track):
        @track.on("ended")
        async def on_ended():
            pc.close()
        @track.on("data")
        async def on_data(data):
            audio_frame = av.AudioFrame.from_ndarray(np.frombuffer(data, np.float32), format="f32")
            audio_data = audio_frame.to_ndarray()
            text = r.recognize_google(audio_data)
            print(text)
    @pc.on("icecandidate")
    def on_icecandidate(candidate):
        pc.add_ice_candidate(candidate)
    pc.setRemoteDescription(offer)
    pc.createAnswer()
    return pc.localDescription.sdp

@app.route("/answer", methods=["POST"])
def answer():
    pc = WebRTCAudioStream()
    pc.setRemoteDescription(RTCSessionDescription.sdp(request.json))
    pc.createAnswer()
    return pc.localDescription.sdp

@app.route("/trickle", methods=["POST"])
def trickle():
    candidate = RTCIceCandidate(request.json)
    pc.add_ice_candidate(candidate)

if __name__ == "__main__":
    app.run(debug=True)
