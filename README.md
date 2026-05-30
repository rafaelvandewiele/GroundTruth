# GroundTruth

Every claim you see — in the news, on social media, from the mouth of a politician — live fact checked in 3 seconds, for everyone in the world, free of charge.

## Gratis tech stack (geen betalingen vereist)

| Onderdeel | Dienst | Limiet |
|-----------|--------|--------|
| AI-model | Google Gemini 1.5 Flash | 1500 requests/dag gratis |
| Webzoeken | DuckDuckGo (scraping) | Geen limiet |
| Database | Supabase | Gratis tier |
| Hosting | Railway | Gratis tot $5/maand gebruik |

## Project Structure

```
groundtruth/
├── backend/
│   ├── app/
│   │   ├── api/routes.py
│   │   ├── core/config.py
│   │   ├── models/schemas.py
│   │   └── services/
│   │       ├── ai_service.py        # Gemini Flash
│   │       ├── search_service.py    # DuckDuckGo
│   │       ├── cache_service.py     # Supabase
│   │       ├── fact_check_service.py
│   │       └── language_service.py
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── supabase_schema.sql
│   └── .env.example
├── app/                             # React Native (Expo)
│   ├── src/
│   │   ├── screens/
│   │   ├── components/
│   │   └── services/
│   ├── App.tsx
│   └── package.json
└── docker-compose.yml
```

## Quick Start

### Stap 1: Gratis Gemini API-sleutel ophalen
Ga naar https://aistudio.google.com → "Get API key" → gratis, geen creditcard nodig.

### Stap 2: Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # vul je Gemini-sleutel en Supabase-keys in
uvicorn main:app --reload
```

### Stap 3: App
```bash
cd app
npm install
npx expo start
```

## Environment Variables (backend/.env)
```
GEMINI_API_KEY=AIza...
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_SERVICE_KEY=eyJ...
```
