from fastapi import FastAPI, File, UploadFile, Form, Body, Header
from fastapi.responses import JSONResponse
from typing import Dict


import wave
import webrtcvad
import io

def is_speech_present(audio_bytes, aggressiveness=3):
    """
    Determines if there is discernible speech in the provided audio bytestream.

    Parameters:
    - audio_bytes (bytes): The audio data in bytes.
    - aggressiveness (int): VAD aggressiveness mode (0-3). Higher values are more aggressive.

    Returns:
    - bool: True if speech is detected, False otherwise.
    """
    # Use BytesIO to read the byte data as a file
    with io.BytesIO(audio_bytes) as audio_file:
        with wave.open(audio_file, 'rb') as wf:
            # Ensure the audio is mono and 16-bit PCM
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000, 32000, 48000]:
                raise ValueError("Audio must be mono, 16-bit PCM, with a sample rate of 8000, 16000, 32000, or 48000 Hz.")
            
            # Read the entire audio data
            audio_data = wf.readframes(wf.getnframes())
            sample_rate = wf.getframerate()

    # Initialize the VAD
    vad = webrtcvad.Vad(aggressiveness)

    # Check for speech in 30ms frames
    frame_duration = 30  # ms
    frame_size = int(sample_rate * frame_duration / 1000) * 2  # 2 bytes per sample
    speech_detected = False

    for i in range(0, len(audio_data), frame_size):
        frame = audio_data[i:i + frame_size]
        if len(frame) < frame_size:
            break
        if vad.is_speech(frame, sample_rate):
            speech_detected = True
            break

    return speech_detected


# Placeholder for processing functions
def process_audio_bytestream(bytestream: bytes) -> Dict:
    # Simulate audio processing
    transcript = "Simulated transcript from bytestream"
    model_thought = "Simulated model thought for bytestream"
    return {"transcript": transcript, "model_thought": model_thought}

def process_audio_file(file_path: str) -> Dict:
    # Simulate processing an audio file
    transcript = "Simulated transcript from file"
    model_thought = "Simulated model thought for file"
    return {"transcript": transcript, "model_thought": model_thought}

def answer_question(question: str) -> str:
    # Simulate answering a question
    return f"Simulated answer for: {question}"

# Initialize FastAPI
app = FastAPI()


from speech_transcription.main import transcribe_audio_object, record_audio, reset, transcribe_audio_bytes
from gpt.prompter import Prompter
import queue  # Use standard thread-safe queue
import openai

import os
# Print the current working directory
print("Current Working Directory:", os.getcwd())
# Print the contents of the current working directory
print("Directory Contents:", os.listdir(os.getcwd()))

'''
with open('API_key.txt', 'r') as file:
    # Read the content and strip any whitespace/newline characters
    openai.api_key = file.readline().strip()
'''
openai.api_key = ''

prompter = Prompter()

transcript_strategy = ["Condensed Transcript: "] # so that we prepend different transcript prompts.
# prepend to prompts to chatgpt. 
content_strategy = [
    'provide a 10 word or less summary of the following content, given the condensed transcript, saying "N" if nothing worth distracting the student showed in the new content: ',
                    ]
question_strategy = [
    "Please answer this question in the context of the lecture: "
]

'''
takes: data as bytestream, condensed_transcript as string ("" if starting)
returns: transcript and insight for data, updated condensed transcript.
'''
@app.post("/process_wav_data/")
async def process_wav_data(data: bytes = Body(...), condensed_transcript: str = Header("")):
    """
    Accepts a wav file as a bytestream and returns a transcript and model thought.
    """
    #if not is_speech_present(data):
        #return {'transcript': "", 'insight':"", 'condensed_transcript':condensed_transcript}
    
    result = transcribe_audio_bytes(data)
    
    result['insight'] = prompter.prompt(messages=[
        {"role":"user", "content": transcript_strategy[0] + condensed_transcript},
        {"role":"user", "content": content_strategy[0] + result['transcript']}
        ])
    
    result['condensed_transcript'] = condensed_transcript + result['insight']
    return JSONResponse(content=result)

@app.post("/process_wav_file/")
async def process_wav_file(file: UploadFile = File(...), condensed_transcript: str = Header("")):
    """
    Accepts a wav file and returns a transcript and model thought.
    """
    # Save the uploaded file temporarily for processing
    #file_path = f"{file.filename}"
    #with open(file_path, "wb") as f:
        #f.write(await file.read())
    x = await file.read()
    #if not is_speech_present(x):
        #return {'transcript': "", 'insight':"", 'condensed_transcript':condensed_transcript}

    result = transcribe_audio_bytes(x)
    result['insight'] = prompter.prompt(messages=[
        {"role":"user", "content": transcript_strategy[0] + condensed_transcript},
        {"role":"user", "content": content_strategy[0] + result['transcript']}
        ])
    
    result['condensed_transcript'] = condensed_transcript + result['insight']
    return JSONResponse(content=result)

@app.post("/question/")
async def process_question(question: str = Form(...), condensed_transcript: str = Header("")):
    """
    Accepts a text question and returns an answer.
    """
    #answer = answer_question(question)
    result = {}
    result['answer'] = prompter.prompt(messages=[
        {"role":"user", "content": transcript_strategy[0] + condensed_transcript},
        {"role":"user", "content": question_strategy[0] + question}
        ])    
    return JSONResponse(content={"answer": result['answer']})
