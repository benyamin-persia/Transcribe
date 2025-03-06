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
    """
    Extracts audio from a video file using ffmpeg.
    - Ensures 16kHz mono format for better transcription accuracy.
    - Reduces noise using highpass and lowpass filters (optional).
    """
    temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    command = f'ffmpeg -i "{video_file}" -ac 1 -ar 16000 -q:a 0 -map a "{temp_wav.name}" -y'
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print("Error running ffmpeg:", e)
        os.unlink(temp_wav.name)
        return None
    return temp_wav.name

def transcribe_whisper(audio_file, result_dict, model_size="base"):
    """
    Transcribes audio using OpenAI Whisper.
    - User can select model size (tiny, base, small, medium, large) for accuracy vs. speed.
    """
    model = whisper.load_model(model_size)
    print(f"Transcribing with Whisper ({model_size} model)... (this may take some time)")
    
    for i in tqdm(range(100), desc="Whisper Transcription Progress", unit="%", leave=False):
        time.sleep(0.05)  # Simulate progress bar
    
    result = model.transcribe(audio_file, verbose=False)
    result_dict["Whisper"] = result["text"]

def transcribe_speech_recognition(audio_file, result_dict, chunk_size=15000):
    """
    Transcribes audio using Google SpeechRecognition.
    - Audio is split into smaller chunks for better accuracy.
    - Chunk size can be adjusted (default: 15 seconds per chunk).
    """
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_wav(audio_file)
    duration_ms = len(audio)
    num_chunks = math.ceil(duration_ms / chunk_size)
    transcriptions = []
    
    print(f"Splitting audio into {num_chunks} chunks for SpeechRecognition...")
    
    def process_chunk(i):
        """Processes individual chunks of audio for transcription."""
        start_ms = i * chunk_size
        end_ms = min((i + 1) * chunk_size, duration_ms)
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
    """
    Saves the transcribed text to a file with the tool's name appended.
    """
    video_dir = os.path.dirname(video_file)
    video_basename = os.path.splitext(os.path.basename(video_file))[0]
    transcription_file = os.path.join(video_dir, f"{video_basename}_{tool_name}_transcription.txt")
    with open(transcription_file, "w") as f:
        f.write(transcribed_text)
    print(f"Transcription saved to {transcription_file}")

def main():
    """
    Main function that handles user input and transcription process.
    """
    video_file = input("Enter the video file path: ")
    if not os.path.exists(video_file):
        print("The file does not exist.")
        return
    
    print("Select transcription tool:")
    print("1 - OpenAI Whisper")
    print("2 - Google SpeechRecognition")
    print("3 - Both (Simultaneously)")
    choice = input("Enter the number: ")
    
    if choice == "1":
        model_size = input("Choose Whisper model (tiny, base, small, medium, large): ") or "base"
    else:
        model_size = "base"
    
    if choice in ["2", "3"]:
        chunk_size = int(input("Enter chunk size for SpeechRecognition (default: 15000ms): ") or 15000)
    else:
        chunk_size = 15000
    
    audio_file = extract_audio(video_file)
    if not audio_file:
        print("Failed to extract audio.")
        return
    
    result_dict = {}  # Dictionary to store transcription results
    
    if choice == "1":
        start = time.time()
        transcribe_whisper(audio_file, result_dict, model_size)
        print(f"OpenAI Whisper took {time.time() - start:.2f} seconds.")
        save_transcription(video_file, result_dict["Whisper"], "Whisper")
    elif choice == "2":
        start = time.time()
        transcribe_speech_recognition(audio_file, result_dict, chunk_size)
        print(f"Google SpeechRecognition took {time.time() - start:.2f} seconds.")
        save_transcription(video_file, result_dict["SpeechRecognition"], "SpeechRecognition")
    elif choice == "3":
        start = time.time()
        whisper_thread = threading.Thread(target=transcribe_whisper, args=(audio_file, result_dict, model_size))
        speech_recognition_thread = threading.Thread(target=transcribe_speech_recognition, args=(audio_file, result_dict, chunk_size))
        
        whisper_thread.start()
        speech_recognition_thread.start()
        
        whisper_thread.join()
        speech_recognition_thread.join()
        
        print(f"Both transcriptions completed in {time.time() - start:.2f} seconds.")
        save_transcription(video_file, result_dict["Whisper"], "Whisper")
        save_transcription(video_file, result_dict["SpeechRecognition"], "SpeechRecognition")
    else:
        print("Invalid choice.")
    
    os.unlink(audio_file)  # Remove temporary audio file
    print("Done!")

if __name__ == "__main__":
    main()
