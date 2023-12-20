
from flask import Flask, render_template, request, jsonify
import os
#import speech_recognition as sr
from openai import OpenAI
client = OpenAI()


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'audio_data' in request.files:
        audio_file = request.files['audio_data']
        audio_path = os.path.join('uploads', audio_file.filename)
        audio_path += '.webm'
        audio_file.save(audio_path)

        # Transcribe audio

        audio_file= open(audio_path, "rb")
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
        # recognizer = sr.Recognizer()
        # with sr.AudioFile(audio_path) as source:
        #     audio_data = recognizer.record(source)
        #     try:
        #         text = recognizer.recognize_google(audio_data)
        #     except sr.UnknownValueError:
        #         text = "Audio not understood"
        #     except sr.RequestError:
        #         text = "Could not request results"

        text = transcript.text
        os.remove(audio_path)  # Remove the audio file after processing
        return jsonify({'transcription': text})

    return jsonify({'transcription': ''})

if __name__ == '__main__':
    app.run(debug=True)
