# WebBuilder

Bouw je website door gewoon te typen wat je wilt. Een AI-website-builder op basis van prompts:
een Next.js-editor met live preview en een Python/FastAPI-backend die de site als gestructureerde
blocks beheert en via een LLM aanpast.

## Architectuur

```
frontend (Next.js)  →  POST /chat  →  backend (FastAPI + LLM-agent)
      │                                        │
      └── iframe: GET /sites/{id}/render        └── site-JSON (blocks) → statische HTML-render
```

De site is opgeslagen als JSON met vaste blok-types (`hero`, `text`, `features`, `gallery`,
`pricing`, `contact`, `footer`) plus een thema (hoofdkleur, lettertype). De AI-agent geeft bij
elke prompt de volledige nieuwe site-JSON terug; de renderer maakt er veilige statische HTML van.

## Mapstructuur

- `backend/` — FastAPI-app (`app/main.py`), Pydantic-schema's, AI-agent (Mistral of OpenAI),
  renderer en opslag (JSON-bestand per omgeving).
- `frontend/` — Next.js App Router: startscherm, chatpaneel en live preview (iframe).

## Draaien

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env        # zet je WEBBUILDER_AI_API_KEY
uvicorn app.main:app --reload
```

De API staat op `http://localhost:8000`. Zonder API-key krijg je bij `/chat` een duidelijke
foutmelding; aanmaken en renderen van sites werkt al wel.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

De editor staat op `http://localhost:3000` en praat met de backend via `NEXT_PUBLIC_API_URL`
(standaard `http://localhost:8000`, zie `frontend/.env.example`).

### Tests

```bash
cd backend
pip install -r requirements.txt pytest
pytest
```

## API-overzicht

| Methode | Endpoint | Functie |
| --- | --- | --- |
| `POST` | `/sites?name=...` | Nieuwe site met standaard blocks |
| `GET` | `/sites` | Alle sites |
| `GET` | `/sites/{id}` | Site als JSON |
| `POST` | `/chat` | Prompt toepassen: `{ siteId, message }` → nieuw site-JSON + uitleg |
| `GET` | `/sites/{id}/render` | Gepubliceerde site als statische HTML |

## Roadmap

1. **Fase 1 (deze versie)** — nieuwe site bouwen via prompts, live preview.
2. **Fase 2** — import van bestaande sites (URL/HTML/WordPress-export → blocks).
3. **Fase 3** — eigen domeinen, versiegeschiedenis met rollback, betalingen.
