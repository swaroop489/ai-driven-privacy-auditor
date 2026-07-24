from fastapi import FastAPI, UploadFile, File, HTTPException
import whisper
import requests
import os
import tempfile
import shutil

from utils.media_processor import extract_audio_from_video

app = FastAPI(title="Multimodal Privacy Service")

model = whisper.load_model("tiny")

NLP_SERVICE_URL = os.environ.get("NLP_SERVICE_URL", "http://localhost:8000/api/v1/predict")
SUPPORTED_EXTENSIONS = ('.mp3', '.wav', '.m4a', '.mp4', '.avi', '.mov', '.mkv')
VIDEO_EXTENSIONS = ('.mp4', '.avi', '.mov', '.mkv')

@app.post("/api/v1/media/transcribe-and-scan")
def transcribe_and_scan(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(SUPPORTED_EXTENSIONS):
        raise HTTPException(status_code=400, detail="Invalid media format")
        
    temp_file_path = None
    audio_file_path = None
    try:
        suffix = os.path.splitext(file.filename)[1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            temp_file_path = tmp.name
            
        if suffix in VIDEO_EXTENSIONS:
            audio_file_path = temp_file_path + "_extracted.mp3"
            success = extract_audio_from_video(temp_file_path, audio_file_path)
            if not success:
                raise HTTPException(status_code=500, detail="Failed to extract audio. Ensure ffmpeg is installed.")
            target_path = audio_file_path
        else:
            target_path = temp_file_path

        result = model.transcribe(target_path)
        transcribed_text = result["text"]
        
        nlp_response = requests.post(
            NLP_SERVICE_URL,
            json={"text": transcribed_text}
        )
        nlp_data = nlp_response.json()
        
        return {
            "transcription": transcribed_text,
            "privacy_scan": nlp_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        if audio_file_path and os.path.exists(audio_file_path):
            os.remove(audio_file_path)
