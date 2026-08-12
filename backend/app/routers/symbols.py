from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Symbol
from ..schemas import SymbolOut

router = APIRouter(prefix="/api/symbols", tags=["symbols"])
#sets up a router, whcih organises my API endpoints. Automatically prepends this path (ap/symbols) to every route in this file.
@router.get("/", response_model=list[SymbolOut]) #decorator,  modifies or wraps that funciton .
#at startup: immediately wraps list_symbols and inspects its arguements and registers the route
#at request: the wrapper intercepts callses, and prepares the databsae connection before formating the output and outputing.
def list_symbols(db: Session = Depends(get_db)):
    return db.query(Symbol).all()

