# ai-ec-agent

Monorepo: FastAPI backend + React frontend.

- [`backend/`](backend/README.md) — FastAPI app (Python), generates the full
  offer→knowledge→strategy→ads/page pipeline described in
  [`APPLICATION_FLOW.md`](APPLICATION_FLOW.md).
- [`frontend/`](frontend/) — React (Vite + TypeScript) app.

## Quick start

Backend:

```bash
cd backend
source venv/bin/activate
python main.py
```

Frontend:

```bash
cd frontend
npm install
cp .env.example .env   # set VITE_API_URL to the backend's URL
npm run dev
```
