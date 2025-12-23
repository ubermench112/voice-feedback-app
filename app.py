import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import whisper

# ------------------------------
# Setup FFmpeg path for audio handling
# ------------------------------
os.environ["PATH"] += os.pathsep + r"C:\Users\91762\Downloads\ffmpeg-8.0.1-essentials_build\ffmpeg-8.0.1-essentials_build\bin"

# ------------------------------
# Flask app configuration
# ------------------------------
app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # limit 50 MB per upload

# ------------------------------
# Load Whisper model (CPU-friendly tiny model)
# ------------------------------
model = whisper.load_model("tiny")  # 'base' can be used for better accuracy

# ------------------------------
# Function to convert audio to text
# ------------------------------
def transcribe_audio(file_path):
    result = model.transcribe(file_path)
    return result["text"]

# ------------------------------
# Simple sentiment analysis based on keywords
# ------------------------------
def analyze_sentiment(text):
    positive_words = ["good", "great", "delicious", "happy"]
    negative_words = ["bad", "poor", "late", "unhappy"]
    score = 0

    for word in positive_words:
        if word in text.lower():
            score += 1

    for word in negative_words:
        if word in text.lower():
            score -= 1

    if score > 0:
        return "Positive"
    elif score < 0:
        return "Negative"
    else:
        return "Neutral"

# ------------------------------
# Routes for the app
# ------------------------------

@app.route("/")
def index():
    # Landing page with record/upload option
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_audio():
    # Check if audio file exists in the request
    if "audio" not in request.files:
        return "No file uploaded", 400

    file = request.files["audio"]
    if file.filename == "":
        return "No selected file", 400

    # Save uploaded file
    filename = secure_filename(file.filename)
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(save_path)

    # Transcribe audio and determine sentiment
    transcription = transcribe_audio(save_path)
    sentiment = analyze_sentiment(transcription)

    # Save transcription to a text file
    transcription_file = os.path.join(app.config["UPLOAD_FOLDER"], filename + ".txt")
    with open(transcription_file, "w", encoding="utf-8") as f:
        f.write(transcription)

    return redirect(url_for("admin"))

@app.route("/admin")
def admin():
    # Admin dashboard showing all uploads, transcriptions, and sentiments
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
    # Serve uploaded files
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# ------------------------------
# Run the app
# ------------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

