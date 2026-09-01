from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from .database import Base, engine
from .routers import symbols, market_data, live_feed, backtest, paper_trade, alerts, ws_alerts
from .services.surveillance_loop import run_surveillance_loop

app = FastAPI(title="ATS Backend")

Base.metadata.create_all(bind=engine)

app.include_router(symbols.router)
app.include_router(market_data.router)
app.include_router(live_feed.router)
app.include_router(backtest.router)
app.include_router(paper_trade.router)
app.include_router(alerts.router)
app.include_router(ws_alerts.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def start_surveillance():
    asyncio.create_task(run_surveillance_loop(ws_alerts.alert_manager.broadcast))

