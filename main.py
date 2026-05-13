from utils.audio_processor import process_input
from core.transcriber import transcribe_chunk

def main():
    print("Welcome to the Gen AI YouTube Transcriber!")
    
    # 1. Ask the user for a YouTube URL
    url = input("Enter a YouTube URL: ")
    
    # 2. Process the audio (download it, convert it, and chunk it)
    print("\nProcessing audio...")
    chunk_files = process_input(url)
    
    # 3. Transcribe each chunk
    print("\nTranscribing chunks...")
    full_transcript = ""
    
    for chunk in chunk_files:
        print(f"Transcribing {chunk}...")
        text = transcribe_chunk(chunk)
        full_transcript += text + " "
        
    print("\n=== FINAL TRANSCRIPT ===")
    print(full_transcript)

# This is the standard Python entry point check
if __name__ == "__main__":
    main()
