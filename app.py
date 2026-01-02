from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from dotenv import load_dotenv
import os
import webbrowser
import threading
import uvicorn

# Load API KEY
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static (index.html inside same folder)
app.mount("/static", StaticFiles(directory="."), name="static")


@app.get("/")
def home():
    return FileResponse("index.html")


@app.post("/api/generate")
async def generate(request: Request):
    try:
        body = await request.json()
        text = body.get("text", "")

        if not text.strip():
            return JSONResponse({"summary": "No text received"}, status_code=400)

        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"Summarize this text in simple English:\n\n{text}"

        response = model.generate_content(prompt)

        return {
            "summary": response.text
        }

    except Exception as e:
        return JSONResponse({"summary": f"Error: {str(e)}"}, status_code=500)


def open_browser():
    webbrowser.open("http://127.0.0.1:9000")


if __name__ == "__main__":
    threading.Timer(1.5, open_browser).start()
    uvicorn.run(app, host="127.0.0.1", port=9000)
