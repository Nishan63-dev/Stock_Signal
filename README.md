# Indian Stock Signals

A real-time stock analysis dashboard for Indian (NSE) stocks providing trading signals (BUY/SELL), dynamic targets, and stop losses based on technical indicators.

## Prerequisites

- Python 3.8+
- `pip`

## Installation

```bash
pip install -r backend/requirements.txt
```

## Running the App

Simply run the provided bash script:

```bash
./run.sh
```

This will start both the backend API and frontend static server.
- **Frontend App**: [http://localhost:3000/index.html](http://localhost:3000/index.html)
- **Backend API**: [http://localhost:8000/api/popular](http://localhost:8000/api/popular)

## Deploying the backend on Render

This repository includes `render.yaml` for a Render web service. When creating the
service, select the repository root as the root directory and use these commands if
you configure the service manually:

```text
Build Command: pip install -r backend/requirements.txt
Start Command: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

Render must provide the `$PORT` value; do not hard-code port `8000` in the start
command. The deployed API will be available at:

```text
https://<your-render-service>.onrender.com/api/popular
```

The root `requirements.txt` also includes `backend/requirements.txt`, so the
existing Render build command `pip install -r requirements.txt` remains compatible.

## Technical Stack
- **Backend**: Python, FastAPI, yfinance, pandas_ta
- **Frontend**: HTML, JavaScript, Tailwind CSS
