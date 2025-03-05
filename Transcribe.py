import subprocess
import speech_recognition as sr
import os
import tempfile
from pydub import AudioSegment
import math

def transcribe_long_audio(audio_file, chunk_length=60):
    """
    Split the audio into chunks, transcribe each, and return the combined transcription.
    """
    audio = AudioSegment.from_wav(audio_file)
    duration_ms = len(audio)
    chunk_ms = chunk_length * 1000  # Convert seconds to milliseconds
    num_chunks = math.ceil(duration_ms / chunk_ms)
    
    recognizer = sr.Recognizer()
    transcriptions = []
    
    print(f"Audio duration: {duration_ms/1000:.2f} seconds, splitting into {num_chunks} chunk(s).")
    
    for i in range(num_chunks):
        start_ms = i * chunk_ms
        end_ms = min((i + 1) * chunk_ms, duration_ms)
        chunk_audio = audio[start_ms:end_ms]
        
        # Save chunk to a temporary file
        chunk_filename = f"chunk_{i}.wav"
        chunk_audio.export(chunk_filename, format="wav")
        
        with sr.AudioFile(chunk_filename) as source:
            audio_data = recognizer.record(source)
        
        try:
            print(f"Transcribing chunk {i+1}/{num_chunks}...")
            chunk_text = recognizer.recognize_google(audio_data, language="en-US")
        except sr.UnknownValueError:
            print(f"Chunk {i+1} not understood.")
            chunk_text = ""
        except sr.RequestError as e:
            print(f"Chunk {i+1} request error: {e}")
            chunk_text = f"Error: {e}"
        
        transcriptions.append(chunk_text)
        os.remove(chunk_filename)
    
    return "\n".join(transcriptions)

# Ask the user for the video file
video_file = input("Please enter the video file path (including the extension): ")

if not os.path.exists(video_file):
    print("The file does not exist.")
    exit(1)

# Create a temporary WAV file for extracted audio
temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
temp_wav_name = temp_wav.name
temp_wav.close()  # Let ffmpeg write to this file

# Build the ffmpeg command to extract audio from the video
command = f'ffmpeg -i "{video_file}" -q:a 0 -map a "{temp_wav_name}"'
print("Running command:", command)

try:
    subprocess.run(command, shell=True, check=True)
except subprocess.CalledProcessError as e:
    print("Error running ffmpeg command:", e)
    os.unlink(temp_wav_name)
    exit(1)

if os.path.getsize(temp_wav_name) == 0:
    print("Extracted audio file is empty. Check if the video contains audio.")
    os.unlink(temp_wav_name)
    exit(1)

# Transcribe the audio in chunks and get the combined transcription
print("Starting transcription...")
full_transcription = transcribe_long_audio(temp_wav_name, chunk_length=60)

# Save the transcription to a text file in the original location of the video file
video_dir = os.path.dirname(video_file)
video_basename = os.path.splitext(os.path.basename(video_file))[0]
transcription_file = os.path.join(video_dir, f"{video_basename}_transcription.txt")

with open(transcription_file, "w") as f:
    f.write(full_transcription)

print(f"\nFull Transcription saved to {transcription_file}")

# Clean up the temporary WAV file
os.unlink(temp_wav_name)
