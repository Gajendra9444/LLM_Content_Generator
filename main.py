import os 
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware


GEMINI_API_KEY = 'Your_API_Key' # Replace with your actual API key
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash-lite")


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContentRequest(BaseModel):
    topic: str
    tone: str = "informative"
    length: str = "medium"    #short | medium | long
    language : str = "en" # defult is English


@app.post("/generate")
def generate_content(request: ContentRequest):
    prompt = f"""Generate a {request.length} article about {request.topic} in a {request.tone} tone. Make it creative, clear, engaging and informative in simple vocabulary in choosen {request.language} language."""
    
    try:
        response = model.generate_content(prompt)
        return {"generated_content": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))