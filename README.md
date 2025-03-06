# Video Transcriber - User Manual

## Overview
This Python script extracts audio from a video file and transcribes it using **OpenAI Whisper** or **Google SpeechRecognition**. Users can select their preferred transcription method and customize settings for better accuracy or speed.

## Features
- **Extracts audio** from video files using `ffmpeg`.
- **Supports two transcription methods:**
  - **OpenAI Whisper** (local AI-based, highly accurate, model size selectable)
  - **Google SpeechRecognition** (cloud-based API, faster for short audio clips)
- **Simultaneous transcription** with both methods for comparison.
- **Progress bar** for real-time feedback.
- **Configurable settings** such as Whisper model size and chunk size for SpeechRecognition.
- **Saves transcriptions** in the same directory as the original video.

## Installation
Ensure you have the required dependencies installed:
```bash
pip install speechrecognition pydub whisper tqdm
```
Additionally, install `ffmpeg` for audio extraction:
```bash
sudo apt install ffmpeg  # Linux
brew install ffmpeg  # macOS
winget install ffmpeg  # Windows
```

## Usage
Run the script and enter the path to the video file:
```bash
python video_transcriber.py
```
Then, choose a transcription method:
```
1 - OpenAI Whisper
2 - Google SpeechRecognition
3 - Both (Simultaneously)
```

### **Choosing an OpenAI Whisper Model**
Whisper offers different model sizes that trade off **speed** vs. **accuracy**. The model you choose affects performance as follows:

| Model   | Speed  | Accuracy  | Size (MB) | Best Use Case |
|---------|--------|-----------|-----------|--------------|
| **tiny**  | 🔥 Fastest | ❌ Least accurate | 39 MB  | Quick previews, short clips, real-time processing |
| **base**  | ⚡ Fast  | ⭕ Medium accuracy | 74 MB  | General use, moderate noise, standard speech |
| **small** | 🚀 Moderate | ✅ Good accuracy | 244 MB | Everyday transcription with better recognition |
| **medium** | 🏎️ Slower | ✅✅ High accuracy | 769 MB | Longer videos, better language handling |
| **large**  | 🐢 Slowest | ✅✅✅ Best accuracy | 1550 MB | High-quality, professional-grade transcription |

**What happens when you choose a model?**
- If you choose **tiny** or **base**, transcription will be **faster** but may **miss words or misinterpret accents**.
- If you choose **small** or **medium**, transcription **slows down slightly** but **accuracy improves**.
- If you choose **large**, transcription **takes the longest** but gives the **most accurate result**.

### **Customization Options**
- **For Whisper:**
  - Choose a model for speed vs. accuracy: `tiny`, `base`, `small`, `medium`, `large`.
- **For Google SpeechRecognition:**
  - Adjust chunk size (default: 15000ms / 15s) to optimize performance.

## Output
The script saves the transcription files in the same directory as the video:
- `{video_filename}_Whisper_transcription.txt`
- `{video_filename}_SpeechRecognition_transcription.txt`

## Notes
- **Whisper** provides the highest accuracy but may be slower.
- **Google SpeechRecognition** is faster but less accurate for longer files.
- **Use smaller chunk sizes** for better Google SpeechRecognition accuracy.

## License
This project is open-source and free to use under the MIT license.

## Author
Developed by [Your Name].

