# MeetingMind AI

A command-line tool that turns a YouTube video or a local audio/video file into a text transcript using OpenAI Whisper, running locally.

## How it works

1. `main.py` asks for a YouTube URL or a file path.
2. `utils/audio_processor.py` gets the audio:
   - a URL is downloaded with `yt-dlp` and saved as WAV
   - a local file is converted to mono, 16 kHz WAV with `pydub`
3. The WAV is split into 10 minute chunks.
4. `core/transcriber.py` transcribes each chunk with Whisper. It can also translate to English (`translate=True`).
5. The chunk texts are joined and printed as the final transcript.

## Project layout

```
main.py                    entry point
core/transcriber.py        Whisper model loading and transcription
utils/audio_processor.py   download, convert and chunk audio
requirements.txt           dependencies
```

## Setup

You need Python 3.10 or newer and [ffmpeg](https://ffmpeg.org) installed (used by `yt-dlp` and `pydub`).

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Set the `WHISPER_MODEL` environment variable to pick a Whisper model size. The default is `base`. Audio is saved in the `downloades/` folder, which is git-ignored.

## Status

Work in progress. `requirements.txt` already lists packages for later features (Streamlit, LangChain, ChromaDB, Mistral, PDF export, Hindi to English translation) that `main.py` does not use yet. Some YouTube videos may need a `cookies.txt` file (git-ignored) to download.
