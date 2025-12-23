# Voice Enabled Customer Feedback Portal

## Problem Overview
I built a web application where users can record and upload their voice feedback. The admin can listen to the recordings, see an automatic transcription, and check the sentiment of the feedback. The goal is to make collecting and analyzing customer feedback simple and faster.

**Example Use Case:**  
A Mumbai-based food delivery service where customers can record their voice feedback about orders. Admins can then review the recordings, the transcription, and the sentiment to improve service quality.

**Cloud Deployment:**  
I also deployed this project on AWS using a serverless setup. When a user uploads a WAV file to an S3 bucket, an AWS Lambda function automatically processes the audio, performs sentiment analysis, and stores the results in a DynamoDB table. This way, the admin can see the results without running the app locally.

---

## Features Implemented
- Simple interface with a "Press to Record" button.
- Uploads audio files to backend, saved in `uploads/` folder.
- Automatic transcription using a local function (currently a placeholder / Whisper).
- Sentiment analysis on transcribed text.
- Admin dashboard to:
  - Play uploaded recordings.
  - View transcriptions.
  - View sentiment.
- Basic separation between user and admin roles.
- Cloud version supports:
  - Uploads to S3 bucket (`voice-feedback-audio-ramanand`)
  - Automatic processing by Lambda (`VoiceFeedbackProcessor`)
  - Storing results in DynamoDB (`DynamoDB`)
  - Monitoring via CloudWatch logs

---

## How the Project Works

### Local Version
1. User records feedback in the frontend.
2. Audio is uploaded to the backend (Flask app).
3. File is saved in `uploads/` folder.
4. Transcription is generated (currently using a dummy function / Whisper).
5. Sentiment is calculated from the transcription.
6. Admin dashboard shows recordings, transcription, and sentiment.

### Cloud Version
1. User uploads a WAV file to the S3 bucket: `voice-feedback-audio-ramanand`.
2. Lambda function `VoiceFeedbackProcessor` triggers automatically.
3. Lambda does the following:
   - Reads the uploaded file from S3.
   - Generates transcription (placeholder for now).
   - Performs sentiment analysis.
   - Saves the data into DynamoDB table `DynamoDB`.
4. Admin can check the results in DynamoDB and monitor the Lambda logs in CloudWatch.

---

## Project Structure
voice-feedback-app/
│
├── app.py             # Main Flask application
├── requirements.txt   # Python dependencies
├── Dockerfile         # Optional, not used for now
├── templates/         # HTML templates
├── uploads/           # Folder for uploaded audio
├── README.md          # This file
└── flowchart.png      # Architecture flowchart

- **Frontend:** HTML + JavaScript (for recording audio)
- **Backend:** Python Flask
- **Transcription:** Whisper (local) / placeholder
- **Sentiment Analysis:** Simple Python logic
- **Storage:** Local `uploads/` folder
- **Cloud Storage & Processing:** AWS S3, Lambda, DynamoDB

---

## Challenges & Decisions
- Whisper transcription is CPU-heavy, so running Docker builds was very slow.
- To save time, transcription was tested locally; AWS Transcribe could be added later.
- Sentiment analysis is simple, keyword-based, but works for basic cases.
- Large audio files may need better optimization.
- Setting up IAM roles for Lambda to write to DynamoDB took some debugging.

---

## How to Run

### Local Version
1. Copy or clone the project folder.
2. Install dependencies:  
```bash
pip install -r requirements.txt

