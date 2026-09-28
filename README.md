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

## Technical Stack
- **Backend**: Python, FastAPI, yfinance, pandas_ta
- **Frontend**: HTML, JavaScript, Tailwind CSS
