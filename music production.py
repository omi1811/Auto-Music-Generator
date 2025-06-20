try:
    from gtts import gTTS
except ImportError:
    print("gTTS is not installed. Please install it with 'pip install gTTS'.")
    exit(1)
import os
import sys

def text_to_speech(text, filename="output.mp3", lang="en"):
    """Convert text to speech and save as an mp3 file. Returns the filename."""
    if os.path.exists(filename):
        response = input(f"Warning: {filename} already exists. Overwrite? (y/n): ").strip().lower()
        if response != 'y':
            print("Operation cancelled.")
            return None
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
        print(f"Saved speech to {filename}")
        # Play the speech (cross-platform)
        if sys.platform.startswith('win'):
            os.system(f'start {filename}')
        elif sys.platform.startswith('darwin'):
            os.system(f'afplay {filename}')
        else:
            os.system(f'xdg-open {filename}')
        return filename
    except Exception as e:
        print(f"Error in text-to-speech: {e}")
        return None

if __name__ == "__main__":
    text = input("Enter text to convert to speech: ")
    lang = input("Enter language code (default 'en'): ") or "en"
    filename = input("Enter output filename (default 'output.mp3'): ") or "output.mp3"
    text_to_speech(text, filename, lang)
