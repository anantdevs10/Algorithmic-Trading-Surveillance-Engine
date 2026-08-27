from fastapi import FastAPI
from .database import Base, engine
from .routers import market_data
from .routers import symbols
from fastapi.middleware.cors import CORSMiddleware
from .routers import live_feed

app = FastAPI(title="ATS Backend")

Base.metadata.create_all(bind=engine)

app.include_router(symbols.router)
app.include_router(market_data.router)
app.include_router(live_feed.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

'''
brings together your database configuration, database models, and API endpoints into a single runnable server
'''