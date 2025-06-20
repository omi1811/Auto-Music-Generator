# Music & Data Processing Utilities

This repository provides utility modules and scripts for music and data processing, including:

- **base_file..py**: A utility module for checking your Python environment and verifying the installation of key music/data science packages.
- **music production.py**: A simple, robust text-to-speech script using gTTS, with cross-platform audio playback and user-friendly features.
- **app.py**: A FastAPI web app for generating music and lyrics using AI APIs (Replicate, Groq).

## Features

- Environment check for common music/data science Python packages
- Text-to-speech with language and filename options
- FastAPI app for AI-powered music and lyrics generation

## Usage

### 1. Environment Check
Run the following to check your Python environment:
```bash
python base_file..py
```

### 2. Text-to-Speech
Run the script and follow the prompts:
```bash
python "music production.py"
```

### 3. FastAPI App
Make sure you have a `.env` file with your API keys:
```
REPLICATE_API_TOKEN=your_replicate_token
GROQ_API_KEY=your_groq_key
```
Then run:
```bash
uvicorn app:app --reload
```

## Requirements
- Python 3.8+
- See `base_file..py` for a list of recommended packages
- gTTS (`pip install gTTS`)
- FastAPI, Uvicorn, Replicate, Groq, python-dotenv

## License
MIT

## Author
Your Name
