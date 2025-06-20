import os
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import replicate
from groq import Groq

load_dotenv()

app = FastAPI()

# Use environment variable names, not actual keys
replicate_api_token = os.getenv("REPLICATE_API_TOKEN")
groq_api_key = os.getenv("GROQ_API_KEY")
if not replicate_api_token or not groq_api_key:
    raise RuntimeError("Missing required API keys in environment variables.")

replicate.api_token = replicate_api_token
client = Groq(api_key=groq_api_key)

# Use relative paths for portability
app.mount("/static", StaticFiles(directory=os.path.join(os.getcwd(), "Static")), name="static")
templates = Jinja2Templates(directory=os.path.join(os.getcwd(), "Templates"))

def generate_lyrics(prompt, language="English"):
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert music lyrics writer. Your task is to create high-quality lyrics that are poetic,emotionally evocative, and tailored to the given theme. Please write the lyrics in " + language + " and keep them concise, under 30 words. Focus on creating imagery and emotion in your words. Do not include any additional text or explanations, just return the lyrics."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=50,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        output = response.choices[0].message.content
        cleaned_output = output.replace("\n", " ")
        formatted_lyrics = f"♪ {cleaned_output} ♪"
        return formatted_lyrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating lyrics: {str(e)}")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate-music")
async def generate_music(prompt: str = Form(...), duration: int = Form(...), language: str = Form(...)):
    try:
        lyrics = generate_lyrics(prompt, language)
        prompt_with_lyrics = lyrics
        output = replicate.run(
            "suno-ai/bark:b76242b40d67c76ab6742e987628a2a9ac019e11d56ab96c4e91ce03b79b2787",
            input={
                "prompt": prompt_with_lyrics,
                "text_temp": 0.73,
                "output_full": True,
                "waveform_temp": 0.7
            }
        )
        # Replicate output is usually a list or generator
        music_url = None
        if isinstance(output, dict) and 'audio_out' in output:
            music_url = output['audio_out']
        elif isinstance(output, (list, tuple)) and len(output) > 0:
            # Try to find a URL in the first element
            first = output[0]
            if isinstance(first, dict) and 'audio_out' in first:
                music_url = first['audio_out']
            elif isinstance(first, str):
                music_url = first
        elif isinstance(output, str):
            music_url = output
        if not music_url:
            raise HTTPException(status_code=500, detail="No audio output returned from Replicate API.")
        return JSONResponse(content={"url": music_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating music: {str(e)}")