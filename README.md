# Market Minds

Market Minds is an AI-assisted portfolio intelligence prototype with:
- Login/signup manager workflow
- Risk-level portfolio classification
- Client-level dashboard with time-series and allocation
- Ticker grouping and alerts
- AI explainability and recommendation timing

## Repository structure

- `frontend/` Streamlit UI app
- `backend/` FastAPI analytics API and risk engine
- `backend/data/` sample CSV datasets

## Run frontend

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

## Run backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Key backend endpoints

- `GET /health`
- `GET /clients`
- `GET /clients/{client_id}/dashboard`
- `GET /risk/{client_id}`
- `GET /risk/summary/metrics`
- `GET /risk/summary/by-ticker`
- `GET /risk/summary/alerts`
- `GET /risk/recommendation/{risk_level}`

## Merge to main

```bash
git checkout main
git pull origin main
git merge work
git push origin main
```
