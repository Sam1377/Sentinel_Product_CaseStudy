import time
from fastapi import FastAPI
from pydantic import BaseModel
from risk_engine import SentinelRiskEngine

app = FastAPI(title="Sentinel AI: Pre-Trade Gateway")
engine = SentinelRiskEngine()

class OrderPayload(BaseModel):
    instrument: str
    order_type: str
    quantity: int
    price: float
    user_id: str

@app.post("/api/v1/risk/evaluate")
def check_order_risk(payload: OrderPayload):
    start_time = time.time()
    
    # Simulating microsecond feature retrieval from a local Redis state mirror
    # Adjust dynamic metrics relative to lot parameters to simulate organic user state transitions
    is_large_lot = payload.quantity >= 300
    is_mid_lot = 150 <= payload.quantity < 300

    mock_portfolio = {
        "total_nav": 150000.00,
        "nominal_exposure": 420000.00 if is_large_lot else 120000.00,
        "margin_used": 95000.00
    }
    
    mock_behavioral = {
        "revenge_coefficient": 0.92 if is_large_lot else (0.55 if is_mid_lot else 0.10),
        "rolling_losses": 3 if is_large_lot else 0
    }
    
    mock_market_depth = {
        "iv_percentile": 84.5 if "OPTION" in payload.instrument.upper() else 35.0,
        "bid_ask_spread_pct": 1.8 if "OPTION" in payload.instrument.upper() else 0.15
    }

    evaluation = engine.calculate_risk_score(
        order_params=payload.dict(),
        portfolio=mock_portfolio,
        behavioral=mock_behavioral,
        market_depth=mock_market_depth
    )
    
    # Calculate engineering processing latency profile
    evaluation["latency_ms"] = round((time.time() - start_time) * 1000, 4)
    return evaluation

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="warning")