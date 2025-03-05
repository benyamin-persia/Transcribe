# Transcribe



---

```markdown
# Video to Transcription Converter

This Python script extracts audio from a video file, splits the audio into manageable chunks, transcribes each chunk using Google's Speech Recognition API, and saves the combined transcription into a text file.

## Features

- **Audio Extraction**: Uses `ffmpeg` to extract audio from video files.
- **Chunking**: Splits long audio into smaller segments (default 60 seconds per chunk) for efficient processing.
- **Speech Recognition**: Transcribes audio using the `speech_recognition` library with Google's Speech-to-Text API.
- **Temporary File Management**: Automatically creates and cleans up temporary audio files.

## Requirements

- **Python 3.6+**
- **ffmpeg**  
  Make sure `ffmpeg` is installed and added to your system's PATH. You can download it from [ffmpeg.org](https://ffmpeg.org/download.html).

- **Python Libraries**
  - [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
  - [pydub](https://pypi.org/project/pydub/)

Install the required Python libraries using pip:

```bash
pip install SpeechRecognition pydub
```

## Usage

1. **Run the Script**

   Execute the script from your terminal or command prompt:

   ```bash
   python your_script_name.py
   ```

2. **Provide Video File**

   When prompted, enter the full path to your video file (including its extension).

3. **Processing**

   The script will:
   - Extract the audio from your video file using `ffmpeg`.
   - Split the extracted WAV audio into 60-second chunks.
   - Transcribe each chunk using Google’s Speech Recognition API.
   - Save the complete transcription in a text file located in the same directory as your video.

4. **Output**

   The transcription will be saved as `video_basename_transcription.txt` (where `video_basename` is the name of your video file without its extension).

## Code Overview

- **Audio Extraction**:  
  The script uses `ffmpeg` to convert the video file into a temporary WAV audio file.
  
- **Chunking**:  
  The `transcribe_long_audio` function utilizes `pydub` to split the audio into chunks, which are then individually transcribed.
  
- **Transcription**:  
  Each audio chunk is transcribed using the `speech_recognition` library’s `recognize_google` method.
  
- **Cleanup**:  
  Temporary files created during the process are removed once they are no longer needed.

## Customization

- **Chunk Length**:  
  You can change the duration of each audio chunk by modifying the `chunk_length` parameter in the `transcribe_long_audio` function.

- **Language**:  
  The default transcription language is set to English (US). To use a different language, change the `language` parameter in the `recognize_google` method.

## Troubleshooting

- **ffmpeg Not Found**:  
  Ensure that `ffmpeg` is installed and correctly added to your system’s PATH.
  
- **Empty Audio File**:  
  If the extracted audio file is empty, verify that the video contains an audio track.
  
- **Speech Recognition Errors**:  
  Check your internet connection as the script uses Google's Speech-to-Text API. Review console output for any error messages.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Google Speech Recognition API](https://cloud.google.com/speech-to-text)
- [ffmpeg](https://ffmpeg.org/)
- [pydub](https://github.com/jiaaro/pydub)
- [SpeechRecognition](https://github.com/Uberi/speech_recognition)
```

---

Feel free to modify the sections as needed to better fit your project's details or add any additional instructions you might have.
