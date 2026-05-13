import yt_dlp
from pydub import AudioSegment
import os

DOWNLOAD_DIR = "downloades"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_youtube_audio(url: str) -> str:
    """
    Downloads audio from a YouTube URL and saves it as a .wav file.
    
    Args:
        url (str): YouTube video URL
    
    Returns:
        str: Path to the downloaded .wav file
    """
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "extractor_args": {"youtube": {"client": ["android", "ios"]}},
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality": "192",
        }],
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace(".webm", ".wav")
    return filename



def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to WAV format using pydub."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_path, format="wav")
    return output_path



def chunk_audio(wav_path:str ,chunk_minutes:int=10)->list:
    """Split wav into chunks.
    Return list of file paths for each chunk.
    """
    audio=AudioSegment.from_wav(wav_path)
    chunk_ms=chunk_minutes *60*1000
    chunks=[]
    for i ,start in enumerate(range(0,len(audio),chunk_ms)):
        chunk=audio[start:start+chunk_ms]
        chunk_path=f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)
        print(chunks)
    return chunks
    
def process_input(source: str) -> list:
    """Process either a YouTube URL or a local file.
    Convert to WAV, split into chunks, and return list of chunk paths.
    """
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Created {len(chunks)} chunks.")
    return chunks





    