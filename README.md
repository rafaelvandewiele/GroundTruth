# GroundTruth

Every claim you see — in the news, on social media, from the mouth of a politician — live fact checked in 3 seconds, for everyone in the world, free of charge.

## Project Structure

```
groundtruth/
├── backend/          # FastAPI Python backend
│   ├── app/
│   │   ├── api/      # Route handlers
│   │   ├── core/     # Config, settings
│   │   ├── models/   # Pydantic models
│   │   └── services/ # AI, search, cache logic
│   ├── requirements.txt
│   └── main.py
├── app/              # React Native (Expo) mobile app
│   ├── src/
│   │   ├── screens/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── services/
│   ├── App.tsx
│   └── package.json
└── docker-compose.yml
```

## Quick Start

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # fill in your API keys
uvicorn main:app --reload
```

### App
```bash
cd app
npm install
npx expo start
```

## Environment Variables (backend/.env)
```
ANTHROPIC_API_KEY=your_key_here
PERPLEXITY_API_KEY=your_key_here
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_KEY=your_supabase_service_key
```
