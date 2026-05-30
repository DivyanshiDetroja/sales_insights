import json
import os
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import anthropic

load_dotenv()

app = FastAPI()

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

SYSTEM_PROMPT = """You are an expert Apple Store B2B sales assistant.
Apple products: iPhone, MacBook, iPad, Apple Watch, AirPods, Vision Pro, accessories.
Services: AppleCare+, trade-in, Business Essentials, education/business pricing.
USPs: ecosystem integration, Genius Bar, premium support.

Analyze the provided client email thread and context. Return ONLY valid JSON in this exact shape:
{
  "insights": ["...", "...", "...", "...", "..."],
  "values": ["...", "...", "..."],
  "experience_tip": "...",
  "pitches": [
    {"tone": "Professional", "speech": "..."},
    {"tone": "Friendly", "speech": "..."},
    {"tone": "Urgent", "speech": "..."}
  ],
  "questions": ["...", "...", "...", "...", "..."]
}

insights: 5 key things the client wants or needs.
values: 3 qualities this client values in companies/products.
experience_tip: one paragraph on how to make the best client experience.
pitches: 2-3 personalized sales speeches in different tones.
questions: 3-5 smart questions the salesperson could ask this client.
"""


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
async def analyze(
    context: str = Form(default=""),
    budget: str = Form(default=""),
    profession: str = Form(default=""),
    email_file: UploadFile = None,
):
    email_thread = ""
    if email_file:
        raw = await email_file.read()
        emails = json.loads(raw)
        for e in emails:
            email_thread += f"From: {e['from']}\nTo: {e['to']}\nDate: {e['date']}\nSubject: {e['subject']}\nBody: {e['body']}\n\n"

    user_content = f"Email thread:\n{email_thread}\n"
    if budget:
        user_content += f"Client budget: {budget}\n"
    if profession:
        user_content += f"Client profession: {profession}\n"
    if context:
        user_content += f"Additional context: {context}\n"

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_content}],
    )

    text = message.content[0].text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    result = json.loads(text)
    return result


app.mount("/", StaticFiles(directory="static", html=True), name="static")
