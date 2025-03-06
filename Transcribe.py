import subprocess
import os
import tempfile
import time
import math
import speech_recognition as sr
from pydub import AudioSegment
import whisper
from tqdm import tqdm
import threading
from concurrent.futures import ThreadPoolExecutor

def extract_audio(video_file):
    """Extracts audio from a video file using ffmpeg."""
    temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    command = f'ffmpeg -i "{video_file}" -ac 1 -ar 16000 -q:a 0 -map a "{temp_wav.name}" -y'
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print("Error running ffmpeg:", e)
        os.unlink(temp_wav.name)
        return None
    return temp_wav.name

def transcribe_whisper(audio_file, result_dict):
    model = whisper.load_model("base")
    print("Transcribing with Whisper... (this may take some time)")
    
    for i in tqdm(range(100), desc="Whisper Transcription Progress", unit="%", leave=False):
        time.sleep(0.05)  # Simulate progress
    
    result = model.transcribe(audio_file, verbose=False)
    result_dict["Whisper"] = result["text"]

def transcribe_speech_recognition(audio_file, result_dict):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_wav(audio_file)
    duration_ms = len(audio)
    chunk_ms = 15000  # Reduce chunk size to 15 seconds for faster parallel processing
    num_chunks = math.ceil(duration_ms / chunk_ms)
    transcriptions = []
    
    print(f"Splitting audio into {num_chunks} chunks for SpeechRecognition...")
    
    def process_chunk(i):
        start_ms = i * chunk_ms
        end_ms = min((i + 1) * chunk_ms, duration_ms)
        chunk_audio = audio[start_ms:end_ms]
        chunk_filename = f"chunk_{i}.wav"
        chunk_audio.export(chunk_filename, format="wav")
        
        with sr.AudioFile(chunk_filename) as source:
            audio_data = recognizer.record(source)
        
        try:
            text = recognizer.recognize_google(audio_data, language="en-US")
        except sr.UnknownValueError:
            text = "[Unrecognized audio]"
        except sr.RequestError as e:
            text = f"[Error: {e}]"
        
        os.remove(chunk_filename)
        return text
    
    with ThreadPoolExecutor() as executor:
        results = list(tqdm(executor.map(process_chunk, range(num_chunks)), total=num_chunks, desc="Processing Audio for Google SpeechRecognition", unit="chunks", leave=False))
    
    result_dict["SpeechRecognition"] = " ".join(results)

def save_transcription(video_file, transcribed_text, tool_name):
    video_dir = os.path.dirname(video_file)
    video_basename = os.path.splitext(os.path.basename(video_file))[0]
    transcription_file = os.path.join(video_dir, f"{video_basename}_{tool_name}_transcription.txt")
    with open(transcription_file, "w") as f:
        f.write(transcribed_text)
    print(f"Transcription saved to {transcription_file}")

def main():
    video_file = input("Enter the video file path: ")
    if not os.path.exists(video_file):
        print("The file does not exist.")
        return
    
    print("Select transcription tool:")
    print("1 - OpenAI Whisper")
    print("2 - Google SpeechRecognition")
    print("3 - Both (Simultaneously)")
    choice = input("Enter the number: ")
    
    audio_file = extract_audio(video_file)
    if not audio_file:
        print("Failed to extract audio.")
        return
    
    result_dict = {}  # Dictionary to store results
    
    if choice == "1":
        start = time.time()
        transcribe_whisper(audio_file, result_dict)
        print(f"OpenAI Whisper took {time.time() - start:.2f} seconds.")
        save_transcription(video_file, result_dict["Whisper"], "Whisper")
    elif choice == "2":
        start = time.time()
        transcribe_speech_recognition(audio_file, result_dict)
        print(f"Google SpeechRecognition took {time.time() - start:.2f} seconds.")
        save_transcription(video_file, result_dict["SpeechRecognition"], "SpeechRecognition")
    elif choice == "3":
        start = time.time()
        whisper_thread = threading.Thread(target=transcribe_whisper, args=(audio_file, result_dict))
        speech_recognition_thread = threading.Thread(target=transcribe_speech_recognition, args=(audio_file, result_dict))
        
        whisper_thread.start()
        speech_recognition_thread.start()
        
        whisper_thread.join()
        speech_recognition_thread.join()
        
        print(f"Both transcriptions completed in {time.time() - start:.2f} seconds.")
        save_transcription(video_file, result_dict["Whisper"], "Whisper")
        save_transcription(video_file, result_dict["SpeechRecognition"], "SpeechRecognition")
    else:
        print("Invalid choice.")
    
    os.unlink(audio_file)
    print("Done!")

if __name__ == "__main__":
    main()
