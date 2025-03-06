# Video Transcriber

This Python script extracts audio from a video file and transcribes it using either OpenAI Whisper or Google SpeechRecognition. Users can choose between these two transcription tools or run both simultaneously for comparison.

## Features
- Extracts audio from video files using `ffmpeg`.
- Transcribes audio using:
  - **OpenAI Whisper** (Local AI-based transcription)
  - **Google SpeechRecognition** (Cloud-based API)
- Runs transcriptions in parallel for improved speed.
- Displays real-time progress bars for transcription.
- Saves transcriptions to a text file in the same directory as the original video.

## Requirements
Make sure you have the following dependencies installed:
```bash
pip install speechrecognition pydub whisper tqdm
```
Additionally, ensure `ffmpeg` is installed:
```bash
sudo apt install ffmpeg  # Linux
brew install ffmpeg  # macOS
winget install ffmpeg  # Windows
```

## Usage
Run the script and provide the video file path:
```bash
python video_transcriber.py
```
Then, select the transcription method:
1. **OpenAI Whisper**
2. **Google SpeechRecognition**
3. **Both (Simultaneously)**

## Output
The transcriptions are saved as:
- `{video_filename}_Whisper_transcription.txt`
- `{video_filename}_SpeechRecognition_transcription.txt`

These files will be located in the same directory as the video.

## Notes
- **Whisper is recommended** for high accuracy but requires a capable system.
- **Google SpeechRecognition** is cloud-based and may be slower.
- Parallel processing has been implemented to speed up Google transcription.

## License
This project is open-source and free to use under the MIT license.

## Author
Developed by [Your Name].

