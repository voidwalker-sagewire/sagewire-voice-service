import os
import subprocess
import tempfile
from flask import Flask, request, send_file, jsonify

app = Flask(__name__)

PIPER_BIN = os.getenv("PIPER_BIN", "piper")
PIPER_MODEL = os.getenv("PIPER_MODEL", "/models/voice.onnx")

@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "sagewire-voice-service",
        "version": "1.0"
    })

@app.post("/speak")
def speak():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "Missing text"}), 400

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as wav:
        wav_path = wav.name

    try:
        subprocess.run(
            [PIPER_BIN, "--model", PIPER_MODEL, "--output_file", wav_path],
            input=text.encode("utf-8"),
            check=True
        )

        return send_file(
            wav_path,
            mimetype="audio/wav",
            as_attachment=False,
            download_name="speech.wav"
        )

    except subprocess.CalledProcessError as e:
        return jsonify({"error": "TTS generation failed"}), 500
