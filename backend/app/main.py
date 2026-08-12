from fastapi import FastAPI
from .database import Base, engine
from .routers import market_data
from .routers import symbols

app = FastAPI(title="ATS Backend")

Base.metadata.create_all(bind=engine)

app.include_router(symbols.router)
app.include_router(market_data.router)

'''
brings together your database configuration, database models, and API endpoints into a single runnable server
'''