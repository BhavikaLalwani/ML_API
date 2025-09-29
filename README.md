# Open Meteo Prediction API

FastAPI app serving two endpoints:
- GET `/predict/rain/?date=YYYY-MM-DD`: rain in exactly +7 days
- GET `/predict/precipitation/fall/?date=YYYY-MM-DD`: cumulated precipitation next 3 days (mm)

## Local run
```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Docker
```bash
docker build -t openmeteo-api .
docker run -p 8000:8000 openmeteo-api
```

## Render
- Connect repo and choose Docker deploy. Dockerfile and `render.yaml` are provided.
- Health check: `GET /health/`

## Models
Place trained models at:
- `app/models/rain_or_not/rf_clf.joblib` (or `.pkl`)
- `app/models/precipitation_fall/rf_reg.joblib` (or `.pkl`)

This app auto-falls back `.joblib` -> `.pkl`.
