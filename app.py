import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import whisper

# ------------------------------
# FFmpeg Path (keep as is if needed)
# ------------------------------
os.environ["PATH"] += os.pathsep + r"C:\Users\91762\Downloads\ffmpeg-8.0.1-essentials_build\ffmpeg-8.0.1-essentials_build\bin"

# ------------------------------
# Flask Setup
# ------------------------------
app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50 MB

# ------------------------------
# Load Whisper model (CPU-friendly tiny version)
# ------------------------------
model = whisper.load_model("tiny")  # change to 'base' if you want more accuracy

# ------------------------------
# Transcription & Sentiment
# ------------------------------
def transcribe_audio(file_path):
    result = model.transcribe(file_path)
    return result["text"]

def analyze_sentiment(text):
    positive = ["good", "great", "delicious", "happy"]
    negative = ["bad", "poor", "late", "unhappy"]
    score = 0
    for w in positive:
        if w in text.lower(): score += 1
    for w in negative:
        if w in text.lower(): score -= 1
    return "Positive" if score > 0 else "Negative" if score < 0 else "Neutral"

# ------------------------------
# Routes
# ------------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_audio():
    if "audio" not in request.files:
        return "No file part", 400

    file = request.files["audio"]
    if file.filename == "":
        return "No selected file", 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(save_path)

    # Debug: check upload
    print("Saved file at:", save_path)
    print("Current files in upload folder:", os.listdir(app.config["UPLOAD_FOLDER"]))

    # Transcription & sentiment (real)
    transcription = transcribe_audio(save_path)
    sentiment = analyze_sentiment(transcription)

    # Save transcription (optional)
    transcription_file = os.path.join(app.config["UPLOAD_FOLDER"], filename + ".txt")
    with open(transcription_file, "w", encoding="utf-8") as f:
        f.write(transcription)

    return redirect(url_for("admin"))

@app.route("/admin")
def admin():
    files = [f for f in os.listdir(app.config["UPLOAD_FOLDER"]) if not f.endswith(".txt")]
    feedback_data = []
    for f in files:
        transcription_path = os.path.join(app.config["UPLOAD_FOLDER"], f + ".txt")
        transcription = ""
        sentiment = ""
        if os.path.exists(transcription_path):
            with open(transcription_path, "r", encoding="utf-8") as tf:
                transcription = tf.read()
            sentiment = analyze_sentiment(transcription)
        feedback_data.append({
            "filename": f,
            "transcription": transcription,
            "sentiment": sentiment
        })
    return render_template("admin.html", feedback_data=feedback_data)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# ------------------------------
# Run App
# ------------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

