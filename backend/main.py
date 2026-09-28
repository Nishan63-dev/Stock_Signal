from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import pandas as pd
import pandas_ta_classic as ta
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def analyze_stock(ticker_symbol: str):
    ticker = yf.Ticker(ticker_symbol)
    # Get 1 month of 5-minute data to have enough history for indicators
    df = ticker.history(period="1mo", interval="15m")
    
    if df.empty:
        raise HTTPException(status_code=404, detail=f"No data found for {ticker_symbol}")
    
    # Calculate indicators
    df.ta.macd(append=True)
    df.ta.atr(append=True)
    df.ta.rsi(append=True)
    df.ta.ema(length=20, append=True)
    df.ta.ema(length=50, append=True)
    
    # Get latest row
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    
    current_price = float(latest['Close'])
    rsi = float(latest['RSI_14'])
    macd = float(latest['MACD_12_26_9'])
    macd_signal = float(latest['MACDs_12_26_9'])
    ema20 = float(latest['EMA_20'])
    ema50 = float(latest['EMA_50'])
    atr = float(latest['ATRr_14'])
    
    signal = "NEUTRAL"
    reason = []
    
    # Simple strategy logic
    if ema20 > ema50 and rsi < 70 and macd > macd_signal:
        signal = "BUY"
        reason.append("Uptrend (EMA20 > EMA50)")
        reason.append("MACD Bullish Crossover")
        if rsi < 30:
            reason.append("Oversold (RSI < 30)")
    elif ema20 < ema50 and rsi > 30 and macd < macd_signal:
        signal = "SELL"
        reason.append("Downtrend (EMA20 < EMA50)")
        reason.append("MACD Bearish Crossover")
        if rsi > 70:
            reason.append("Overbought (RSI > 70)")
            
    # Calculate Target and Stop Loss using ATR (Average True Range)
    target = None
    stop_loss = None
    
    if signal == "BUY":
        stop_loss = current_price - (1.5 * atr)
        target = current_price + (3 * atr) # 1:2 risk reward
    elif signal == "SELL":
        stop_loss = current_price + (1.5 * atr)
        target = current_price - (3 * atr)
        
    return {
        "ticker": ticker_symbol,
        "current_price": round(current_price, 2),
        "signal": signal,
        "reasons": reason,
        "target": round(target, 2) if target else None,
        "stop_loss": round(stop_loss, 2) if stop_loss else None,
        "indicators": {
            "rsi": round(rsi, 2) if not pd.isna(rsi) else None,
            "macd": round(macd, 2) if not pd.isna(macd) else None,
            "ema20": round(ema20, 2) if not pd.isna(ema20) else None,
            "ema50": round(ema50, 2) if not pd.isna(ema50) else None,
            "atr": round(atr, 2) if not pd.isna(atr) else None
        },
        "last_updated": str(latest.name)
    }

@app.get("/api/analyze/{symbol}")
def get_analysis(symbol: str):
    # Ensure it has .NS for NSE
    if not symbol.endswith(".NS") and not symbol.endswith(".BO"):
        symbol = symbol + ".NS"
    return analyze_stock(symbol)

@app.get("/api/popular")
def get_popular():
    popular_stocks = ["RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK"]
    results = []
    for stock in popular_stocks:
        try:
            res = analyze_stock(f"{stock}.NS")
            results.append(res)
        except Exception as e:
            print(f"Error analyzing {stock}: {e}")
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
