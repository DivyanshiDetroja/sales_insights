# Sales Proposal Personalization Engine — CLAUDE.md

## What this app is
A local, desktop-only B2B sales tool for an Apple Store rep.
No auth. No login. No users. No mobile/tablet support. No analytics.

Salesman inputs context + uploads a JSON email thread → Claude API analyzes → returns structured client insights + personalized pitches.

---

## Tech Stack
- **Backend**: Python + FastAPI (`main.py`)
- **Frontend**: Plain HTML/CSS/JS in `static/index.html` (from Google Stitch)
- **AI**: Anthropic Claude API (`claude-sonnet-4-6`)
- **Dev server**: `uvicorn main:app --reload` → `http://localhost:8000`

---

## Business Context (Apple Store — baked into system prompt)
Products: iPhone, MacBook, iPad, Apple Watch, AirPods, Vision Pro, accessories
Services: AppleCare+, trade-in, Business Essentials, education/business pricing
USPs: ecosystem integration, Genius Bar, premium support

---

## Email JSON Format (for fake demo data)
```json
[
  {
    "from": "name@company.com",
    "to": "sales@applestore.com",
    "subject": "...",
    "body": "...",
    "date": "YYYY-MM-DD"
  }
]
```
Files live in `dummy_data/` — use these for demo and testing.

---

## Claude API Response Shape
The `/analyze` endpoint asks Claude to return strict JSON:
```json
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
```

---

## Build Order (do NOT skip ahead — test each before moving on)
1. Project scaffold + `/health` endpoint
2. JSON email parser utility
3. `/analyze` POST endpoint + Claude integration
4. Frontend input page (placeholder)
5. Frontend output page (render Claude response)
6. Swap in Google Stitch design

---

## Key Rules
- No abstractions, no tests, no error handling beyond what's needed for the happy path
- No comments unless the WHY is non-obvious
- Budget and profession are optional — if not in email, Claude defaults to generic premium positioning
- Web search is MOCKED — do not add real search APIs
- Do not add any analytics, charts, or dashboards
- Keep code as simple as possible
